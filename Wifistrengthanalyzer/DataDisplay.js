import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const DataDisplay = ({selectedAccessPoint,displayDistance = true,displayRSSI = true,displayHeatmap = true,data, }) => {
  const measuredPower = -35;
  const N = 2.3;
  
  return (
    <View style={styles.container}>
      {/* Selected Access Point */}
      {selectedAccessPoint && (
        <View style={styles.section}>
          <Text style={styles.header}>Selected Access Point:</Text>
          <Text>MAC: {selectedAccessPoint.mac}</Text>
          <Text>SSID: {selectedAccessPoint.SSID}</Text>
        </View>
      )}

      {/* Distance */}
      {displayDistance && (
        <View style={styles.section}>
          <Text style={styles.header}>Distance:</Text>
          <Text>{Math.pow(10, (measuredPower - selectedAccessPoint.RSSI) / (10 * N))} m</Text>
        </View>
      )}

      {/* RSSI */}
      {displayRSSI && (
        <View style={styles.section}>
          <Text style={styles.header}>RSSI:</Text>
          <Text>{selectedAccessPoint.RSSI} dBm</Text>
        </View>
      )}

      {/* Heatmap */}
      {displayHeatmap && (
        <View style={styles.section}>
          <Text style={styles.header}>Heatmap:</Text>
          {/* You can render your heatmap here */}
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginTop: 20,
  },
  section: {
    marginBottom: 15,
  },
  header: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 5,
  },
});

export default DataDisplay;