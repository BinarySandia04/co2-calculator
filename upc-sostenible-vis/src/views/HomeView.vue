<script setup>
import CenteredSlot from '../components/slots/CenteredSlot.vue';

import Api from '@/services/Api.js'

import { ref } from 'vue';

const from = ref("");
const to = ref("");
const errorMessage = ref("")
const loadingMessage = ref("")

const dataPresent = ref(false)

const time = ref("");
const km = ref("");
const co2 = ref("");

function login(){
  var fromText = from.value;
  var toText = to.value;

  console.log(fromText + " " + toText);

  errorMessage.value = ""
  loadingMessage.value = "La teva petició està sent processada. Espera uns segons..."
  dataPresent.value = false;

  Api().post('/calc', { from: fromText, to: toText }).then((response) => {
    loadingMessage.value = ""
    dataPresent.value = true;
    const data = response.data;

    time.value = data["time"];
    km.value = data["dist"];
    co2.value = data["co2"];

    console.log(data);
  }).catch((error) => {
    loadingMessage.value = ""
    errorMessage.value = "Alguna de les direccions que has introduït no és vàlida";
  });
}

// Carrer Aribau, 8, Barcelona
// Carrer Pau Gargallo, Barcelona

</script>

<template>
  <CenteredSlot>
    <img class="upc-logo" src="upc_logo_white.png">
    <h1>Calculadora de viatje sostenible CO2</h1>

    <p class="message error-message" v-if="errorMessage">{{ errorMessage }}</p>
    <p class="message loading-message" v-if="loadingMessage">{{ loadingMessage }}</p>

    <form v-on:submit.prevent="login">
        <div class="form-field">
            <label for="from">Introdueix la direcció d'origen</label>
            <input id="from-field" type="text" placeholder="Carrer Aribau, 8, Barcelona" name="from" v-model="from" autocomplete="off" >
        </div>
        <div class="form-field">
            <label for="to">Introdueix la direcció de destí:</label>
            <input id="from-field" type="text" placeholder="Carrer Pau Gargallo" name="to" v-model="to" autocomplete="off" >
        </div>
        <br class="sep">
        <div class="form-field">
            <button class="btn-primary">Enviar</button>
        </div>
    </form>

   <!-- <div v-if="dataPresent" class="bento-container"> -->
  

  </CenteredSlot>
  <div class="bento-container">
    <div class="bento-item time-container">
      <span>232132321</span>
    </div>
    <div class="bento-item dist-container">
      <span>32132113</span>
    </div>
    <div class="bento-item co2-container">
      <span>321321312</span>
    </div>

  </div> 
</template>


<style scoped lang="scss">

.bento-container {
  display: flex;
  flex-direction: row;
  width: 1000px;
  margin-left: auto;
  margin-right: auto;
}

.bento-item {
  flex-grow: 1;

  background-color: var(--color-background-semisoft);
}

.upc-logo {
  width: 200px;
  height: 200px;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 30px;
}

.message {

  padding-top: 14px;
  padding-bottom: 14px;
  border-radius: 8px;
  text-align: center;
  font-size: 18px;
  
  &.error-message {
    color: #da7878;
    background-color: rgba(78, 46, 46, 0.4);
  }

  &.loading-message {
    color: rgb(218, 172, 120);
    background-color: rgba(78, 67, 46, 0.4);
  }
}


.form-field {
    display: flex;
    flex-direction: column;
    min-width: 600px;
    margin-top: 20px;
}

.sep {
  margin-bottom: 28px;
}

h1 {
  margin-bottom: 32px;
}

</style>
