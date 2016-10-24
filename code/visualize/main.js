const electron = require('electron');
const {app} = electron;
const {BrowserWindow} = electron;

let win;

function createWindow() {
    win = new BrowserWindow({width: 1280, height: 780, show: false});
    win.setMenu(null);
    win.loadURL(`file://${__dirname}/ui/index.html`);

    win.on('closed', () => {
        win = null;
    });

    win.once('ready-to-show', () => {
        win.show()
    })
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
    app.quit();
});

app.on('activate', () => {
    if(win === null) {
        createWindow();
    }
});