import api from "../api"
const axios = require('axios')
import { AsyncStorage } from 'react-native'

async function refreshToken() {
  await api.get('imgurToken/')
  .then(res => {        
    AsyncStorage.setItem('imgur_access_token', res.data.value)
  })
}

/*
  Sube una imagen codificada en base64 a Imgur,
  retorna la url de la imagen si salio todo bien;
  Si retorna 'recall' hay que llamar de vuelta al metodo (se va a refreshear el token)
  Si retorna 'error' hubo un error y no se completo la funcion con exito
*/
async function uploadImage(encodedimg) {
  let access_token = await AsyncStorage.getItem('imgur_access_token')
  let url = ''
  if ( access_token === "null" ) {
    await refreshToken()
  }  
  await axios({
    method: 'post',
    url: 'https://api.imgur.com/3/image',
    data: {
      image: encodedimg
    },
    headers: {
      Authorization: `Bearer ${access_token}`
    }
  })
  .then( response => { 
    if (response.status === 200) {
      url = response.data.data.link
    }
    else if ((response.status === 400 && response.data.error.code === 500) || response.status === 403 ) {
      AsyncStorage.setItem('imgur_access_token', "null")
      url = 'recall'
    }
    else {      
      url = 'errorUncatched'
    }
  })
  .catch( error => {
    url = 'errorCatched'
  })
  return url
}

async function handleImageUpload(image) {
  
  // Saque regex de web, porque en mobile me dan bien la data de la imagen
  const encondedAvatar = image
  
  let avatar_url = "URL NO ASIGNADA"
  avatar_url = await uploadImage(encondedAvatar)
  if (avatar_url === 'recall') {
    avatar_url = await uploadImage(encondedAvatar)
  }

  return avatar_url
}


function getImagen(url) {
  return url
}


export { uploadImage, getImagen, handleImageUpload }