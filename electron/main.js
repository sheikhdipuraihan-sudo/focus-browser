const { app, BrowserWindow, WebContentsView, ipcMain, session, dialog, shell } = require('electron');
const path = require('node:path');
const fs = require('node:fs');

const partition = 'persist:focus';
let win, chromeView, tabs = [], active = -1;
const extensionState = () => path.join(app.getPath('userData'), 'extensions.json');
function loadExtensionPaths(){ try { return JSON.parse(fs.readFileSync(extensionState(),'utf8')); } catch { return []; } }
function saveExtensionPaths(paths){ fs.writeFileSync(extensionState(), JSON.stringify(paths, null, 2)); }
function send(channel, payload){ if (win && !win.isDestroyed()) win.webContents.send(channel, payload); }
function createWindow(){
  win = new BrowserWindow({width:1400,height:900,backgroundColor:'#202124',webPreferences:{preload:path.join(__dirname,'preload.js'),contextIsolation:true,nodeIntegration:false}});
  chromeView = new WebContentsView({webPreferences:{preload:path.join(__dirname,'preload.js'),contextIsolation:true,nodeIntegration:false}});
  win.contentView.addChildView(chromeView); chromeView.setBounds({x:0,y:0,width:1400,height:900}); chromeView.webContents.loadFile(path.join(__dirname,'renderer/index.html'));
  win.on('resize', ()=>{ const [w,h]=win.getContentSize(); chromeView.setBounds({x:0,y:0,width:w,height:h}); });
  createTab('https://www.google.com/');
}
function createTab(url){
  const view = new WebContentsView({webPreferences:{partition, contextIsolation:true, nodeIntegration:false}});
  tabs.push({view,url});
  view.webContents.setWindowOpenHandler(({url})=>{createTab(url);return {action:'deny'};});
  view.webContents.on('did-navigate', (_e,u)=>send('tab-update',{index:tabs.findIndex(t=>t.view===view),url:u,title:view.webContents.getTitle()}));
  view.webContents.on('page-title-updated', (_e,title)=>send('tab-update',{index:tabs.findIndex(t=>t.view===view),url:view.webContents.getURL(),title}));
  view.webContents.on('did-start-loading',()=>send('loading',true)); view.webContents.on('did-stop-loading',()=>send('loading',false));
  view.webContents.loadURL(url); setActive(tabs.length-1); send('tabs', tabs.map((t,i)=>({index:i,title:t.view.webContents.getTitle()||'New Tab',url:t.view.webContents.getURL()})));
}
function setActive(i){ if(i<0||i>=tabs.length)return; active=i; tabs.forEach((t,j)=>j===i?win.contentView.addChildView(t.view):win.contentView.removeChildView(t.view)); const [w,h]=win.getContentSize(); tabs[i].view.setBounds({x:0,y:72,width:w,height:h-72}); send('active-tab',{index:i,url:tabs[i].view.webContents.getURL()}); }
app.whenReady().then(async()=>{ const ses=session.fromPartition(partition); for(const p of loadExtensionPaths()){ try{await ses.extensions.loadExtension(p);}catch(e){console.error('Extension load failed',p,e.message);} } createWindow(); });
app.on('window-all-closed',()=>{if(process.platform!=='darwin')app.quit();});

ipcMain.on('navigate',(_e,text)=>{let url=text.trim(); if(!/^https?:\/\//i.test(url)){url=/\s/.test(url)?`https://www.google.com/search?q=${encodeURIComponent(url)}`:`https://${url}`;} tabs[active]?.view.webContents.loadURL(url);});
ipcMain.on('new-tab',(_e,url='https://www.google.com/')=>createTab(url));
ipcMain.on('switch-tab',(_e,i)=>setActive(i));
ipcMain.on('close-tab',(_e,i)=>{if(tabs.length===1)return; const t=tabs.splice(i,1)[0]; t.view.webContents.close(); setActive(Math.max(0,Math.min(active,tabs.length-1))); send('tabs',tabs.map((x,j)=>({index:j,title:x.view.webContents.getTitle()||'New Tab',url:x.view.webContents.getURL()})));});
ipcMain.on('go-back',()=>tabs[active]?.view.webContents.goBack()); ipcMain.on('go-forward',()=>tabs[active]?.view.webContents.goForward()); ipcMain.on('reload',()=>tabs[active]?.view.webContents.reload());
ipcMain.handle('install-extension', async()=>{const r=await dialog.showOpenDialog(win,{properties:['openDirectory']});if(r.canceled)return null;const p=r.filePaths[0];try{const ext=await session.fromPartition(partition).extensions.loadExtension(p);const paths=loadExtensionPaths();if(!paths.includes(p)){paths.push(p);saveExtensionPaths(paths);}return {id:ext.id,name:ext.name};}catch(e){return {error:e.message};}});
ipcMain.handle('list-extensions',()=>session.fromPartition(partition).extensions.getAllExtensions().map(x=>({id:x.id,name:x.name,version:x.version}))); ipcMain.handle('remove-extension',async(_e,id)=>{await session.fromPartition(partition).extensions.removeExtension(id);return true;});
session.fromPartition(partition).on('will-download',(_e,item)=>{item.setSavePath(path.join(app.getPath('downloads'),item.getFilename()));item.once('done',(_e,state)=>send('download-done',{name:item.getFilename(),state}));});
