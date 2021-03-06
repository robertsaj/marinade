const electron = require('electron');
const fs = require('fs');
var client;
// Module to control application life.
const app = electron.app;
// Connect to live update if LIVE_UPDATE env variable is true
if (process.env.LIVE_UPDATE === "true") {
  app.commandLine.appendSwitch('remote-debugging-port', '8315');
  client = require('electron-connect').client;
}
const protocol = electron.protocol;
// Module to create native browser window.
const BrowserWindow = electron.BrowserWindow;

const path = require('path');
const url = require('url');

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow;

function createWindow () {
  //Intercept any urls on the page and find the file on disk instead
  protocol.interceptFileProtocol('file', function(req, callback) {
    var url = req.url.substr(7);
    callback({path: path.normalize(__dirname + url)});
  },function (error) {
    if (error) {
      console.error('Failed to register protocol');
    }
  });

  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 700,
    //titleBarStyle: 'hidden-inset',
    "web-preferences": {
      "web-security": false
    }
  });

  // and load the index.html of the app.
  mainWindow.loadURL(url.format({
    pathname: 'index.html',
    protocol: 'file:',
    slashes: true
  }));

  // Open the DevTools.
  if (process.env.OPEN_DEV_TOOLS === "true") {
    mainWindow.webContents.openDevTools();
  }

  // Emitted when the window is closed.
  mainWindow.on('closed', function () {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    mainWindow = null;
  });

  // Connect to live update if LIVE_UPDATE env variable is true
  if (client) {
    client.create(mainWindow, {"sendBounds":false});
  }

  mainWindow.maximize();
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow);

// Quit when all windows are closed.
app.on('window-all-closed', function () {
  // On OS X it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', function () {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (mainWindow === null) {
    createWindow();
  }
});

let pyProc = null;
let pyPort = null;

const selectPort = () => {
  pyPort = 4242;
  return pyPort
};

const createPyProc = () => {
  let port = '' + selectPort();
  let script = path.join(__dirname, 'backend', 'main.py');
  console.log(script);
  pyProc = require('child_process').spawn('python', [script, port],{
    // send console output to the javascript console
    detached: true,
    stdio: [ 'ignore', 1, 2 ]
  });
  if (pyProc !== null) {
    console.log('child process success');
  }
};

const exitPyProc = () => {
  pyProc.kill();
  pyProc = null;
  pyPort = null;
};

app.on('ready', createPyProc);
app.on('will-quit', exitPyProc);

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.

// Application Inter-Process Communication (IPC) Functions

// Fucntion triggered when Angular requests saving a new file
electron.ipcMain.on('saveNewFile', (event, fileContents) => {
  console.log('DEBUG: Save new file');
  electron.dialog.showSaveDialog(
    mainWindow,
    {
      title: 'Save File',
      defaultPath: process.env['HOME'] + '/code',
      filters: [
        { name: 'ARM ASM', extensions: [ 's' ] }
      ]
    },
    (filename) => {
      if (filename) {
        fs.writeFile(filename, fileContents, (error) => {
          if (error) { console.log('Error ', error); }
        });
        event.sender.send('saveNewFileCallback', filename);
      }
    }
  );
});

electron.ipcMain.on('saveFile', (event, fileFullPath, fileContents) => {
  console.log('DEBUG: Save file');
  fs.truncate(fileFullPath, (error) => {
    if (error) { console.log(error); }
    fs.writeFile(fileFullPath, fileContents, (error) => {
      if (error) { console.log(error); }
    });
  });
  event.sender.send('saveFileCallback');
});

electron.ipcMain.on('openFile', () => {
  electron.dialog.showOpenDialog(
    mainWindow,
    {
      title: 'Open File',
      defaultPath: process.env['HOME'] + '/Workspace/marinade/dist/config/architectures',
      filters: [
        { name: 'JSON', extensions: [ 'json' ] }
      ]
    },
    (filename) => {
      if (filename) {
        fs.readFile(filename[0], 'utf8', (error, data) => {
          if (error) {
            console.log('Error ', error);
          } else {
            mainWindow.webContents.send('openFileCallback', data, filename[0]);
          }
        });
      }
    }
  )
});

electron.ipcMain.on('showError', (event, title, content) => {
  electron.dialog.showErrorBox(title, content);
});

electron.ipcMain.on('showMessage', (event, title, content) => {
  electron.dialog.showMessageBox(mainWindow, {
    type: 'info',
    title: title,
    message: content
  })
});

// Relay commands to communicate between Angular components
electron.ipcMain.on('saveRequest', (event) => {
  event.sender.send('saveRequest');
});
electron.ipcMain.on('compileRequest', (event) => {
  event.sender.send('compileRequest');
});
electron.ipcMain.on('runRequest', (event) => {
  event.sender.send('runRequest');
});
