const http = require("http");
const fs = require("fs");
const path = require("path");
const root = __dirname;
const port = Number(process.env.PORT || 3000);
const types = {".html":"text/html; charset=utf-8",".css":"text/css; charset=utf-8",".js":"text/javascript; charset=utf-8",".json":"application/json; charset=utf-8",".svg":"image/svg+xml"};
http.createServer((req,res)=>{
  let pathname;
  try { pathname = decodeURIComponent(new URL(req.url, "http://localhost").pathname); } catch { res.writeHead(400); return res.end("Bad request"); }
  if (pathname === "/health" || pathname === "/healthz") { res.writeHead(200,{"content-type":"application/json"}); return res.end(JSON.stringify({status:"ok",service:"vocal-vibe-ai"})); }
  let file = path.join(root, pathname === "/" ? "index.html" : pathname);
  if (!file.startsWith(root + path.sep) && file !== path.join(root,"index.html")) { res.writeHead(403); return res.end("Forbidden"); }
  fs.stat(file,(err,stat)=>{
    if(err || !stat.isFile()){ res.writeHead(404,{"content-type":"text/plain; charset=utf-8"}); return res.end("Not found"); }
    res.writeHead(200,{"content-type":types[path.extname(file)]||"application/octet-stream","x-content-type-options":"nosniff","referrer-policy":"strict-origin-when-cross-origin","cache-control":path.basename(file)==="index.html"?"no-cache":"public, max-age=3600"});
    fs.createReadStream(file).pipe(res);
  });
}).listen(port,"0.0.0.0",()=>console.log("VocalVibe AI listening on "+port));