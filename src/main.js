// import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
const app = createApp(App)

app.use(router)

app.mount('#app')
app.config.errorHandler = (err)=>{
    console.log("il y a une erreur Error:", err)
}
axios.defaults.withCredentials = true
axios.defaults.baseURL = "http://localhost:8005/"


