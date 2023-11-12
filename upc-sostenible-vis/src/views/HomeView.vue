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
const co2_car = ref("");

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

    var h = parseFloat(data["time"]);
    var m = parseInt(h * 60) % 60;

    var finalTime = "";
    if(h != 0) finalTime += Math.round(h) + "h";
    if(m != 0) finalTime += " " + m + "m";

    var finalKm = (Math.round(parseFloat(data["dist"]) * 100) / 100) + " km";
    var finalCo2 = (Math.round(parseFloat(data["co2"]) * 1000) / 1000) + " kg";
    var finalCo2Car = (Math.round(parseFloat(data["car_emissions"]) * 1000) / 1000) + " kg";

    time.value = finalTime;
    km.value = finalKm;
    co2.value = finalCo2;
    co2_car.value = finalCo2Car;

    console.log(data);

    setTimeout(() => {
      window.scrollTo(0, document.body.scrollHeight);
    }, 10);
  }).catch((error) => {
    loadingMessage.value = ""
    errorMessage.value = "Alguna de les direccions que has introduït no és vàlida";
  });
}

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
            <input id="from-field" type="text" placeholder="Biblioteca de la FME, Barcelona" name="from" v-model="from" autocomplete="off" >
        </div>
        <div class="form-field">
            <label for="to">Introdueix la direcció de destí:</label>
            <input id="from-field" type="text" placeholder="Gran via de les corts catalanes, 585, Barcelona" name="to" v-model="to" autocomplete="off" >
        </div>
        <br class="sep">
        <div class="form-field">
            <button class="btn-primary">Enviar</button>
        </div>
    </form>

  </CenteredSlot>

  <div v-if="dataPresent">
    <div class="other-text margin-fix">
      <h1>Un viatge sostenible tindria...</h1>
    </div>
    <div class="bento-container">
      <div class="bento-item time-container">
        <p class="big">CO2 🏭</p>

        <div class="progress">
        </div>
        <span class="text-element">{{ co2 }}</span>
      </div>
      <div class="bento-item dist-container">
        <p class="big">Distància 🛣️</p>
        <div class="progress">
        </div>
        <span class="text-element">{{ km }}</span>
      </div>
      <div class="bento-item co2-container">
        <p class="big">Temps ⌚</p>
        <div class="progress">
        </div>
        <span class="text-element">{{ time }}</span>
      </div>
    </div>
    <div class="other-text margin-fix-2">
      <h1 id="bottom">En canvi, el viatge en cotxe produiria {{ co2_car }} de CO2</h1>
    </div>
  </div>
</template>


<style scoped lang="scss">

.other-text {
  text-align: center;
  &.margin-fix {
    margin-top: -200px;
    margin-bottom: 200px;
  }
}

.margin-fix-2 {
  margin-top: -20px;
  padding-bottom: 80px;
}

.big {
  font-size: 48px;
  font-weight: bold;
  max-width: auto;
}

.progress {

  margin-left: auto;
  margin-right: auto;
  margin-top: 50px;

  width: 250px;
  height: 250px;
  border-radius: 50%;
  background-color: var(--color-background-softest);

  
}
.text-element {
    position: relative;
    text-align: center;
    bottom: 152px;
    margin-left: 5px;
    display: block;
    font-weight: bold;
    font-size: 32px;

  }

.progress::after {
  width: 230px;
  height: 230px;
  content: '';
  position: relative;
  display: block;
  inset: 10px;
  border-radius: 50%;
  background-color: var(--color-background-semisoft);
}

.bento-container {
  margin-top: -140px;
  display: flex;
  flex-direction: row;
  width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.bento-item {
  flex-grow: 1;

  max-width: 400px;

  min-height: 500px;
  margin-bottom: 100px;
  padding: 20px;
  margin-right: 10px;
  margin-left: 10px;
  border-radius: 8px;

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
