<template>
  <div id="app">
    <Ssl/>
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import Configs from './configs/common'
import Ssl from './components/Ssl.vue'

export default {
  metaInfo: {
    title: Configs.CNAME,
    titleTemplate: Configs.CNAME,
    htmlAttrs: {
      lang: 'ja',
      amp: true
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'application-name', content: Configs.CNAME },
      { name: 'robot', content: 'noindex,nofollow' },
      { name: 'author', content: 'ketoha' },
      { name: 'copyright', content: '&copy;ketoha' },
      { name: 'og:site_name', content: Configs.CNAME },
      { name: 'og:url', content: Configs.CURL },
      { name: 'og:title', content: Configs.CNAME }
    ]
  },
  name: 'App',
  components: {
    Ssl
  }
}
</script>

<style>
@import "../public/index.css";
</style>
