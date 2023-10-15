import React from 'react';
import { View, Text, Switch, StyleSheet } from 'react-native';

const DisplayOptions = ({ displayDistance, displayRSSI, displayHeatmap, onToggleDisplay }) => {
  return (
    <View style={styles.container}>
      {/* Header */}
      <Text style={styles.header}>Display Options:</Text>
      
      {/* Distance Toggle */}
      <View style={styles.optionContainer}>
        <Text>Distance</Text>
        <Switch
          value={displayDistance}
          onValueChange={() => onToggleDisplay('distance')}
        />
      </View>
      
      {/* RSSI Toggle */}
      <View style={styles.optionContainer}>
        <Text>RSSI</Text>
        <Switch
          value={displayRSSI}
          onValueChange={() => onToggleDisplay('rssi')}
        />
      </View>
      
      {/* Heatmap Toggle */}
      <View style={styles.optionContainer}>
        <Text>Heatmap</Text>
        <Switch
          value={displayHeatmap}
          onValueChange={() => onToggleDisplay('heatmap')}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginTop: 20,
  },
  header: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  optionContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
});

export default DisplayOptions;