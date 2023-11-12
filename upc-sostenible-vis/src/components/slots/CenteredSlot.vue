<script setup>
</script>

<template>
    <div class="form-field">
  <slot></slot>
  </div>
</template>

<style scoped>
.form-field {
    height: 100%;
    max-width: 700px;

    margin-left: auto;
    margin-right: auto;
    display: flex;
    flex-direction: column;
    min-width: 600px;
    margin-top: 20px;

    justify-content: center;
}

.centered {
    text-align: center;
}

.underline {
    text-decoration: underline;
}

</style>