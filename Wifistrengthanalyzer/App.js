import React, { useState, useEffect } from 'react'; 
import { View, Text, Button, StyleSheet, ActivityIndicator} from 'react-native';
import AccessPointSelection from './AccessPointSelection';
import { fetchAccessPoints } from './AccessPointSelection';
import DisplayOptions from './DisplayOptions';
import DataDisplay from './DataDisplay';

const App = () => {
  // State variables
  const [accessPoints, setAccessPoints] = useState([]);
  const [showAccessPointSelection, setShowAccessPointSelection] = useState(false); // Initialize to false
  const [displayDistance, setDisplayDistance] = useState(false);
  const [displayRSSI, setDisplayRSSI] = useState(false);
  const [displayHeatmap, setDisplayHeatmap] = useState(false);
  const [data, setData] = useState({ ap_rssi: -1, distance: null });
  const [scanning, setScanning] = useState(false);
  const [selectedAccessPoint, setSelectedAccessPoint] = useState(null);
  const [loading, setLoading] = useState(false); // Scanning state
  const API_URL = 'https://192.168.104.171/:8000';

  // Fetch access points when the component mounts
  useEffect(() => {
    // Wrap the API call in a function to handle loading state
    const fetchAccessPointsData = async () => {
      setLoading(true); // Set loading to true while fetching
      try {
        const data = await fetchAccessPoints();
        setAccessPoints(data);
      } catch (error) {
        console.error('Error fetching access points:', error);
      } finally {
        setLoading(false); // Set loading to false when fetching is complete
      }
    };

    fetchAccessPointsData();
  }, []);

  const handleShowAccessPoints = () => {
    // Set showAccessPointSelection to true to render the component
    setShowAccessPointSelection(true);
  };

  // Handle access point selection
  const onSelectAccessPoint = async (ap) => {
    setSelectedAccessPoint(ap);
    console.log('Selected Access Point:', ap);
    //alert(ap.RSSI)
    try {
      const response = await fetch(`${API_URL}/get_data?ap_mac=${ap.mac}`);
      if (response.ok) {
        const data = await response.json();
        setData(data);
      } else {
        const responseBody = await response.text();
        console.error('Error fetching data for the selected access point. Status Code:', response.status);
        console.error('Response Body:', responseBody);
      }
    } catch (error) {
      //console.error('API request error:', error);
    }
  };

  // Toggle display options
  const onToggleDisplay = (option) => {
    if (option === 'distance') {
      setDisplayDistance(!displayDistance);
    } else if (option === 'rssi') {
      setDisplayRSSI(!displayRSSI);
    } else if (option === 'heatmap') {
      setDisplayHeatmap(!displayHeatmap);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>WiFi Access Point Data</Text>
      <Button title="Scan Access Points" onPress={handleShowAccessPoints} />
      {loading ? ( // Display loading indicator while fetching
        <ActivityIndicator size="large" color="#0000ff" />
      ) : showAccessPointSelection ? (
        <AccessPointSelection onSelectAccessPoint={onSelectAccessPoint} />
      ) : (
        <Text></Text>
      )}
      <DisplayOptions
        displayDistance={displayDistance}
        displayRSSI={displayRSSI}
        displayHeatmap={displayHeatmap}
        onToggleDisplay={onToggleDisplay}
      />
      <DataDisplay
        selectedAccessPoint={selectedAccessPoint}
        displayDistance={displayDistance}
        displayRSSI={displayRSSI}
        displayHeatmap={displayHeatmap}
        data={data}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center', 
    alignItems: 'center', 
    padding: 20,
  },
  header: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
});

export default App;