<template>
    <div class ="Library">
      <p>test shit</p>
      <ol>
        <li v-for="site in sites">
          {{site.name}}
        </li>
      </ol>

    </div>
</template>

<script>
    export default {
      name: 'Library',
      data() {
        return {
          sites: [
            {name: 'Runoob'},
            {name: 'Google'},
            {name: 'Taobo'},
          ]
        }
      }
    }
</script>

<style scoped>
  h1, h2 {
    font-weight: normal;
  }
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    display: inline-block;
    margin: 0 10px;
  }
  a {
    color: #b94834;
  }
</style>
