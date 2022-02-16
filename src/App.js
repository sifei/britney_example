import React, { useEffect, useState } from 'react'
import { API } from 'aws-amplify'

import logo from './logo.svg';
import './App.css';

function App() {
  const [songs, setSongs] = useState([])

  useEffect(() => {
    const getData = async () => {
      const data2 = await API.post('britneySongApi', '/song/', { body: { name: 'Everytime', year: '2003', link: 'https://www.youtube.com/watch?v=8YzabSdk7ZA' } })
      console.log(data2)

      const data = await API.get('britneySongApi', '/song')
      setSongs(data.data.Items)


    }

    getData()
  }, [])
  return (
    <div className="App">
      <h1 className="pink-text">Britney Spears Songs</h1>
      {songs.map(song => (
        <div key={song.id.S}>
          <h2>{song.name.S}</h2>
          <iframe width='560' height='315' src={song.link.S.replace('watch?v=', 'embed/')} frameBorder='0' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture' allowFullScreen />
        </div>
      ))}
    </div>
  )
}

export default App;
