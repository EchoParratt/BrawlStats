import axios from 'axios';
import chai from 'chai';
const { expect } = chai;

describe('Backend Integration Tests', function () {
  this.timeout(30000); // Increase timeout to 30 seconds

  it('should fetch player data from the API and interact with the database', async function () {
    try {
      const playerTag = '#8J2Y2VCC'
      const response = await axios.get(`http://127.0.0.1:5000/player/${encodeURIComponent(playerTag)}`); 
      console.log('Response data:', response.data);
      expect(response.status).to.equal(200);
      expect(response.data).to.be.an('object');
      expect(response.data).to.have.property('name');
    } catch (error) {
      if (error.response) {
        console.error('Response error:', error.response.data);  // Detailed response error
        console.error('Status:', error.response.status);  // HTTP status code
        console.error('Headers:', error.response.headers);  // Response headers
      } else if (error.request) {
        console.error('Request error:', error.request);  // Request error
      } else {
        console.error('Error:', error.message);  // General error
      }
      console.error('Error config:', error.config);  // Error configuration
      throw new Error(error);
    }
  });

  // More tests can be added here...
});
