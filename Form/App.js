import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TextInput, Button, FlatList, TouchableOpacity, Alert } from 'react-native';

const API_URL = 'http://10.16.36.76:5000/v1/usuarios/';

export default function App() {
  const [usuarios, setUsuarios] = useState([]);
  const [id, setId] = useState('');
  const [nombre, setNombre] = useState('');
  const [edad, setEdad] = useState('');
  const [editando, setEditando] = useState(false);

  useEffect(() => {
    leerUsuarios();
  }, []);


  const leerUsuarios = async () => {
    try {
      const response = await fetch(API_URL);
      const data = await response.json();
      setUsuarios(data.usuarios);
    } catch (error) {
      Alert.alert("Error", "No se pudo conectar con el servidor");
    }
  };

  const guardarUsuario = async () => {
    if (!id || !nombre || !edad) return Alert.alert("Error", "Llena todos los campos");

    const metodo = editando ? 'PUT' : 'POST';
    const urlFinal = editando ? `${API_URL}${id}` : API_URL;

    try {
      const response = await fetch(urlFinal, {
        method: metodo,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: parseInt(id), nombre, edad: parseInt(edad) }),
      });

      if (response.ok) {
        Alert.alert("Éxito", editando ? "Actualizado" : "Creado");
        limpiarFormulario();
        leerUsuarios();
      } else {
        const errorData = await response.json();
        Alert.alert("Error", errorData.detail || "Error en la operación");
      }
    } catch (error) {
      console.error(error);
    }
  };

  const eliminarUsuario = async (idEliminar) => {
    try {
      const response = await fetch(`${API_URL}${idEliminar}`, { method: 'DELETE' });
      if (response.ok) {
        leerUsuarios();
      }
    } catch (error) {
      Alert.alert("Error", "No se pudo eliminar");
    }
  };

  const seleccionarUsuario = (item) => {
    setId(item.id.toString());
    setNombre(item.nombre);
    setEdad(item.edad.toString());
    setEditando(true);
  };

  const limpiarFormulario = () => {
    setId(''); setNombre(''); setEdad(''); setEditando(false);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.titulo}>CRUD Usuarios FastAPI</Text>

      <View style={styles.formulario}>
        <TextInput style={styles.input} placeholder="ID" value={id} onChangeText={setId} keyboardType="numeric" editable={!editando} />
        <TextInput style={styles.input} placeholder="Nombre" value={nombre} onChangeText={setNombre} />
        <TextInput style={styles.input} placeholder="Edad" value={edad} onChangeText={setEdad} keyboardType="numeric" />

        <Button title={editando ? "Actualizar" : "Crear Usuario"} onPress={guardarUsuario} />
        {editando && <Button title="Cancelar" color="red" onPress={limpiarFormulario} />}
      </View>

      <FlatList
        data={usuarios}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text>{item.nombre} - {item.edad} años (ID: {item.id})</Text>
            <View style={styles.botonesCard}>
              <TouchableOpacity onPress={() => seleccionarUsuario(item)}>
                <Text style={{ color: 'blue', marginRight: 15 }}>Editar</Text>
              </TouchableOpacity>
              <TouchableOpacity onPress={() => eliminarUsuario(item.id)}>
                <Text style={{ color: 'red' }}>Eliminar</Text>
              </TouchableOpacity>
            </View>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, paddingTop: 50, paddingHorizontal: 20, backgroundColor: '#f5f5f5' },
  titulo: { fontSize: 22, fontWeight: 'bold', marginBottom: 20, textAlign: 'center' },
  formulario: { marginBottom: 30, backgroundColor: '#fff', padding: 15, borderRadius: 10, elevation: 3 },
  input: { borderBottomWidth: 1, borderColor: '#ccc', marginBottom: 10, padding: 5 },
  card: { backgroundColor: '#fff', padding: 15, marginBottom: 10, borderRadius: 8, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  botonesCard: { flexDirection: 'row' }
});