import React, { useState } from 'react';
import axios from 'axios';
import belle_icon from "./assets/Belle_Portrait.webp";  
import leon_icon from "./assets/Leon_Portrait.webp";
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
        <div className = 'trophies'>
        <p>Trophies: {playerData.trophies}</p>
        </div>
        <p>Club: {playerData.club}</p>
        <div className = 'winrate'>
        <p>Win Rate: <span className="win-rate">{playerData.win_rate}</span></p>
        </div>
        <p>Most Played Brawler: {playerData.most_played_brawler} ({playerData.most_played_count} times)</p>
        <img src={belle_icon}/>
        <div className = 'winRatio'>
        <p>Highest Win Ratio Brawler: {playerData.highest_win_ratio_brawler} ({playerData.highest_win_ratio})</p>
        </div>
        <img src={leon_icon}/>
      </div>}
    </div>
  );
}

export default App;


