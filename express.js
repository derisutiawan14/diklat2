// const express = require('express')
// const app = express()
// const port = 3000

// app.get('/',(req, res) => res.send('Hello World!'))

// app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))

// const express = require('express')
// const app = express()

// app.get('/',function(req, res) {
//     res.send("Hello World!")
// })

// app.listen(3000, function() {
//     console.log("Server Nyala")
// })

// const express = require('express')
// const app = express()

// app.get('/',(req, res) => {
//     res.send('Hello World!')
// })

// app.get('/products', (req, res) => {
//     res.json([
//         "Apple",
//         "Redmi",
//         "One Plus One"
//     ])
// })

// app.get('/orders', (req, res) => {
//     res.json([
//         {
//             id: 1,
//             paid: false,
//             user_id: 1
//         },
//         {
//             id: 2,
//             paid: false,
//             user_id: 1
//         },
//     ])
// })

// app.listen(3000, () => {
//     console.log("Server Nyala")
// })

// const express = require('express')
// const app = express()

// app.set('view engine', 'ejs')

// app.get('/greet', (req, res) => {
//     const name = req.query.name || 'Void'
//     res.render('indexs', {
//         name
//     })
// })

// app.listen(3000, () => {
//         console.log("Server Nyala")
//     })

const express = require('express')
const app = express()
const users = []

app.set('view engine','ejs')

app.use(express.urlencoded({ extended: false}))

app.get('/', (req,res) => {
    res.send(`Jumlah user ${users.length}`)
})

app.get('/register', (req,res) => {
    res.render('indexs')
})

app.post('/register', (req,res) => {
    const { email, password} = req.body

    users.push({ email, password })
    res.redirect('/')
})

app.listen(3000, () => {
    console.log("jalan ni")
    })