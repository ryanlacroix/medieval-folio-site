var path = require('path');
const express = require('express')
const app = express()

// Accomodate for local and remote deployment
let port = process.env.PORT;
if (port == null | port == "") {
    port = 8000
}

/*app.defaultConfiguration('*.css', (req, res) => {
    // Add code to grab query and get file
})*/

app.use(express.static('public'))

// Digital Edition (exhibit page)
app.get('/', (req, res) => {
    console.log(req)
    res.sendFile(path.join(__dirname, './public', 'home.html')) 
})

app.get('*', function(req, res){
    res.status(404).sendFile(path.join(__dirname, './public', '404.html'), 404);
});

app.listen(port, () => console.log(`kt's website running on port ${port}`))