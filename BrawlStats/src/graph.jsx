import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto'; // This is needed for Chart.js v3 and above

function TrophyGraph({ playerTag }) {
  const [trophyData, setTrophyData] = useState([]);
  const [startingTrophies, setStartingTrophies] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/player/${encodeURIComponent(playerTag)}`);
        const { trophy_changes, starting_trophies } = response.data;
        console.log("Fetched Trophy Changes:", trophy_changes); // Debugging line
        console.log("Fetched Starting Trophies:", starting_trophies); // Debugging line
        setTrophyData(trophy_changes);
        setStartingTrophies(starting_trophies);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [playerTag]);

  const cumulativeTrophies = trophyData.reduce((acc, change) => {
    const lastValue = acc.length > 0 ? acc[acc.length - 1] : startingTrophies;
    return [...acc, lastValue + change];
  }, []);

  console.log('Cumulative Trophies:', cumulativeTrophies); // Debugging line

  const data = {
    labels: Array.from({ length: trophyData.length }, (_, i) => `Game ${i + 1}`),
    datasets: [
      {
        label: 'Trophy Progression',
        data: cumulativeTrophies,
        fill: false,
        borderColor: '#ffc107',
        tension: 0.1
      }
    ]
  };

  const options = {
    plugins: {
      legend: {
        display: false // Remove the blue box outline (legend)
      }
    },
    scales: {
      x: {
        ticks: {
          color: '#B6B6B8', // Change the color of the text (labels)
          font: {
            size: 12, // Change font size
            family: 'Roboto Mono', // Change font family
          }
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.2)', // Change the color of the grid lines
        }
      },
      y: {
        ticks: {
          color: '#B6B6B8', // Change the color of the text (labels)
          font: {
            size: 12, // Change font size
            family: 'Roboto Mono', // Change font family
          }
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.2)', // Change the color of the grid lines
        }
      }
    }
  };


  return <Line data={data} options = {options} />;
}

export default TrophyGraph;
