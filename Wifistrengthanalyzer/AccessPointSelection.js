import React, { useEffect, useState, useRef } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet } from 'react-native';

// Function to fetch access points with error handling
export async function fetchAccessPoints() {
  try {
    const response = await fetch('http://192.168.104.171:8000/get_aps');
    
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    
    const data = await response.json();
    console.log('API Response Data:', data);
    return data.access_points || {};
  } catch (error) {
    console.error('Error fetching access points:', error.message);
    throw error; // Re-throw the error for further handling if needed
  }
}

const AccessPointSelection = ({ onSelectAccessPoint }) => {
  const [accessPoints, setAccessPoints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [key, setKey] = useState(Math.random().toString());
  const componentRef = useRef(null);

  useEffect(() => {
    // Fetch access points when the component mounts
    fetchAccessPoints()
      .then((data) => {
        // Convert the access points object into an array for rendering
        const accessPointsArray = Object.entries(data).map(([mac, info]) => ({
          mac,
          ...info,
        }));
        setAccessPoints(accessPointsArray);

        if (componentRef.current) {
          componentRef.current.forceUpdate();
        }

        setLoading(false);
        setKey(Math.random().toString());
        console.log('Access points:', accessPointsArray);
      })
      .catch((error) => {
        console.error('Error fetching access points:', error);
        setLoading(false);
      });
  }, []);

  return (
    <View key={key} style={styles.container}>
      <Text style={styles.header}>Select an Access Point:</Text>
      {loading ? (
        <Text>Loading access points...</Text>
      ) : accessPoints.length > 0 ? (
        <FlatList
          data={accessPoints}
          keyExtractor={(item) => [item.mac,item.ssid]}
          renderItem={({ item }) => (
            <TouchableOpacity
              onPress={() => onSelectAccessPoint(item)}
              style={styles.accessPointItem}
            >
              <Text>{item.SSID}</Text>
            </TouchableOpacity>
          )}
        />
      ) : (
        <Text>No access points found.</Text>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  accessPointItem: {
    padding: 10,
    marginVertical: 5,
    borderWidth: 1,
    borderColor: 'gray',
    borderRadius: 5,
  },
});

export default AccessPointSelection;
