const fs = require('fs');
const https = require("https");
const StreamZip = require('node-stream-zip');
var path = require('path');



var platform = process.platform.toLowerCase();
var arch = process.arch.toLowerCase();
console.log(platform)
console.log(arch)

let downloads = JSON.parse(fs.readFileSync('fullDownloads.json')).downloads;

var type = 'lite';
var clientHome;

var latest = downloads.platform[platform].latest
async function setup(){
    downloads.platform[platform].versions.forEach(function(file) {
        if (file.version == latest && file.type == type) {
            console.log(file.download)
            var url = file.download;
            var filename = file.download.split('/').pop();
            var filepath = './' + filename;
            var file = fs.createWriteStream(filepath);
            https.get(url, function(response) {
                response.pipe(file);
                file.on('finish', function() {
                    file.close();
                   // x = extract(filename, { dir: process.cwd()})        
                   const zip = new StreamZip.async({ file: filename });
                    zip.on('extract', (entry, file) => {
                        if ( ! clientHome ) {
                            clientHome = path.dirname(entry.name);
                        }
                    });                 

                     zip.extract(null, '.').then(() => {
                        console.log('done');
                        testDB();
                     })
                    //console.log(x.files)
                });
                 
            })
                
        }
    });
}

 setup();
function testDB(){
    console.log("db..." + clientHome)
    const oracledb = require('oracledb');
     oracledb.initOracleClient({libDir: process.cwd() + "/" + clientHome,configDir: __dirname});
     dbConfig = {
               user: "klrice",
               connectString: "localhost:1521/xe",
               password : "klrice"
             };
    connection =  oracledb.getConnection(dbConfig).then(function(connection) {
        console.log("Connected to Oracle Database");
        var sql = "select "+i+" from dual";
        connection.execute( sql).then(function(result) {
            console.log(results);
        })
    })
}

