import React, { useState } from 'react';
import axios from 'axios';
import belle_icon from "./assets/Belle_Portrait.webp";  
import leon_icon from "./assets/Leon_Portrait.webp";
import jessie_icon from "./assets/Jessie_Portrait.webp"
import spike_icon from "./assets/Spike_Portrait.webp"
import trophy_icon from "./assets/trophy.webp"
import club_icon from"./assets/Ranking.webp"
import info_icon from"./assets/Info-Round.png"
import './App.css';


function App() {
  const [playerTag, setPlayerTag] = useState('');
  const [playerData, setPlayerData] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.get(`http://127.0.0.1:5000/player/${encodeURIComponent(playerTag)}`);
      setPlayerData(response.data);  // Axios automatically parses JSON data
      setError('');
    } catch (e) {
      // Check if the error is because of Axios or a network problem
      if (e.response) {
        // The request was made and the server responded with a status code
        // that is not in the range of 2xx
        setError(e.response.data.error || 'An error occurred');
      } else if (e.request) {
        // The request was made but no response was received
        setError('No response from server');
      } else {
        // Something happened in setting up the request that triggered an Error
        setError(e.message);
      }
      setPlayerData(null);
    }
  };

  return (
    <div>
    <h1>BrawlStats</h1>
    <div className ='top-right-icon'>
    <img src={info_icon} alt="info-icon"/>
    </div>
    <div className='container'>
      <form onSubmit={handleSubmit}>
        <input
          value={playerTag}
          onChange={e => setPlayerTag(e.target.value)}
          placeholder="Enter Player Tag"
          required
        />
        <button type="submit">Get Player Stats</button>
      </form>
      {error && <p>Error: {error}</p>}
      {playerData && <div>
        <p>Name: {playerData.name}</p>
        <div className = 'icon-and-text'>
        <p>Trophies: {playerData.trophies}</p>
        <img src={trophy_icon} alt="Trophy" className="icon-small"/>
        </div>
        <div className ='icon-and-text'>
        <p>Club: {playerData.club}</p>
        <img src={club_icon} alt="Club" className="icon-small"/>
        </div>
        <div className = 'winrate'>
        <p>Win Rate: <span className="win-rate">{playerData.win_rate}</span></p>
        </div>
        <p>Most Played Brawler: {playerData.most_played_brawler} ({playerData.most_played_count} times)</p>
        <img className = 'mpb'src={spike_icon}/>
        <div className = 'winRatio'>
        <p>Highest Win Ratio Brawler: {playerData.highest_win_ratio_brawler} ({playerData.highest_win_ratio})</p>
        </div>
        <img className = 'wrb' src={jessie_icon}/>
      </div>}
    </div>
    </div>

  );
}

export default App;


