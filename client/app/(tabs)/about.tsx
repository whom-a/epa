import { Text, View, StyleSheet } from 'react-native';
import { Link } from 'expo-router';
export default function AboutScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>About Screen</Text>
      <Link href="/about" style={styles.button}>
        Go to Home Screen
      </Link>
    </View>
  );
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#00ffff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  text: {
    color: '#eee',
  },
  button: {
    fontSize: 25,
    textDecorationLine: 'underLine',
    color: '#000',
  },
});