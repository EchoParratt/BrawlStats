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
import jacky_icon from "./assets/Jacky_Portrait.webp"
import meg_icon from "./assets/Meg_Portrait.webp"
import sandy_icon from "./assets/Sandy_Portrait.webp"
import mrp_icon from "./assets/Mr._P_Portrait.webp"
import sam_icon from "./assets/Sam_Portrait.webp"
import byron_icon from "./assets/Byron_Portrait.webp"

import { square } from 'ldrs'

square.register()

// Default values shown

import TrophyGraph from './graph.jsx';
import './App.css';

function App() {
  const [playerTag, setPlayerTag] = useState('');
  const [playerData, setPlayerData] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false); 


  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log("Form submitted with playerTag:", playerTag);
    setLoading(true);
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
    } finally {
      setLoading(false); // Set loading to false after the request completes
    }
  };
  
  const brawlerIcons = {
    BELLE: belle_icon,
    LEON: leon_icon,
    JESSIE: jessie_icon,
    SPIKE: spike_icon,
    FRANK: frank_icon,
    SQUEAK: squeak_icon,
    HANK: hank_icon,
    LILY: lily_icon,
    DOUG: doug_icon,
    BUSTER: buster_icon,
    'MR. P': mrp_icon,
    SAM: sam_icon,
    MEG: meg_icon,
    SANDY: sandy_icon,
    JACKY: jacky_icon,
    BYRON: byron_icon

    // Add other mappings as necessary
  };

  const getBrawlerIcon = (brawlerName) => {
    return brawlerIcons[brawlerName] || leon_icon; // Return the brawler icon or a default icon if not found
  };


  return (
    <div className="app-container">
      {loading && (
        <div className="loading-container">
          <l-square
            size="70"
            stroke="10"
            stroke-length="0.25"
            bg-opacity="0.1"
            speed="1.2"
            color="#aa00ff"
          ></l-square>
        </div>
      )}
      {!loading && (
      <div className="header">
        <h1>BrawlStats</h1>
      </div>
      )}
      {!loading && !playerData && (
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
      {!loading && playerData && (
        <div className="content-container">
          <div className="box left-box">
            <h2>Trophy Progression</h2>
            <TrophyGraph playerTag={playerTag}/>
          </div>
          <div className="box middle-box">
            <h2>Player Information</h2>
            <p><strong>Name:</strong> {playerData.name}</p>
            <p><strong>Trophies:</strong> {playerData.trophies}<strong><img src ={trophy_icon} className='icon-small'/></strong></p>
            <p><strong>Club:</strong> {playerData.club}<strong><img src = {club_icon} className='icon-small'/></strong></p>
            <p><strong>Win Rate:</strong> {playerData.win_rate}</p>
            <p><strong>Most Played:</strong> {playerData.most_played_brawler}</p>
            <img className='mpb' src={getBrawlerIcon(playerData.most_played_brawler)} alt="Most Played Brawler" />
            <p><strong>Most Wins:</strong> {playerData.highest_win_ratio_brawler} <strong>/</strong> {playerData.highest_wins}</p>
            <img className='wrb' src={getBrawlerIcon(playerData.highest_win_ratio_brawler)} alt="Best Win Rate Brawler" />
          </div>
          <div className="box right-box">
            <h2>Current Meta</h2>
            {playerData.top_8_brawlers && playerData.top_8_brawlers.map((brawler, index) => (
              <div key={index} className ='brawler-info'>
                <span className="brawler-name">{brawler.name}</span>
                <span className='brawler-win-rate'>Win Rate: {brawler.winRate}</span>
                <span><img src={getBrawlerIcon(brawler.name.toUpperCase())} className="brawler-image" alt={brawler.name} /></span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

