import React, { useState } from 'react';
import axios from 'axios';
import belle_icon from "./assets/Belle_Portrait.webp";  
import leon_icon from "./assets/Leon_Portrait.webp";
import jessie_icon from "./assets/Jessie_Portrait.webp";
import spike_icon from "./assets/Spike_Portrait.webp";
import trophy_icon from "./assets/trophy.webp";
import club_icon from "./assets/Ranking.webp";
import info_icon from "./assets/Info-Round.png";
import frank_icon from "./assets/Frank_Portrait.webp";
import squeak_icon from "./assets/Squeak_Portrait.webp";
import hank_icon from "./assets/Hank_Portrait.webp";
import lily_icon from "./assets/Lily_Portrait.webp"
import doug_icon from "./assets/Doug_Portrait.webp"
import buster_icon from "./assets/Buster_Portrait.webp"
import './App.css';

function App() {
  const [playerTag, setPlayerTag] = useState('');
  const [playerData, setPlayerData] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log("Form submitted with playerTag:", playerTag);
    try {
      const response = await axios.get(`http://127.0.0.1:5000/player/${encodeURIComponent(playerTag)}`);
      console.log("Data received from server:", response.data);
      setPlayerData(response.data);  // Axios automatically parses JSON data
      setError('');
    } catch (e) {
      console.error("Error occurred:", e);
      if (e.response) {
        setError(e.response.data.error || 'An error occurred');
      } else if (e.request) {
        setError('No response from server');
      } else {
        setError(e.message);
      }
      setPlayerData(null);
    }
  };
  
  const brawlerIcons = {
    Belle: belle_icon,
    Leon: leon_icon,
    Jessie: jessie_icon,
    Spike: spike_icon,
    Frank: frank_icon,
    Squeak: squeak_icon,
    Hank: hank_icon,
    Lily: lily_icon,
    Doug: doug_icon,
    Buster: buster_icon,
    // Add other mappings as necessary
  };

  const getBrawlerIcon = (brawlerName) => {
    return brawlerIcons[brawlerName] || default_icon; // Return the brawler icon or a default icon if not found
  };


  return (
    <div className="app-container">
      <div className="header">
        <h1>BrawlStats</h1>
      </div>
      {!playerData && (
        <div className="input-container">
          <form onSubmit={handleSubmit}>
            <input
              value={playerTag}
              onChange={e => setPlayerTag(e.target.value)}
              placeholder="Enter Player Tag"
              required
            />
            <button type="submit">Get Player Stats</button>
          </form>
        </div>
      )}
      {error && <p className="error-message">{error}</p>}
      {playerData && (
        <div className="content-container">
          <div className="box left-box">
            {/* Placeholder for future content or left content */}
          </div>
          <div className="box middle-box">
            <h2>Player Information</h2>
            <p><strong>Name:</strong> {playerData.name}</p>
            <p><strong>Trophies:</strong> {playerData.trophies}</p>
            <p><strong>Club:</strong> {playerData.club}</p>
            <p><strong>Win Rate:</strong> {playerData.win_rate}</p>
            <p><strong>Most Played:</strong> {playerData.most_played_brawler}</p>
            <img className='mpb' src={belle_icon} alt="Most Played Brawler" />
            <p><strong>Best Win Rate:</strong> {playerData.highest_win_ratio_brawler}</p>
            <img className='wrb' src={leon_icon} alt="Best Win Rate Brawler" />
          </div>
          <div className="box right-box">
            <h2>Top 3 Brawlers</h2>
            {playerData.top_3_brawlers && playerData.top_3_brawlers.map((brawler, index) => (
              <div key={index} className ='brawler-info'>
                <span className="brawler-name">{brawler.name}</span>
                <span className='brawler-win-rate'>Win Rate: {brawler.winRate}</span>
                <span><img src={getBrawlerIcon(brawler.name)} className="brawler-image" alt={brawler.name} /></span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;


