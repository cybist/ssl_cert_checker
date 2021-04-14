<template>
  <div>
    <h1>SSL証明書 更新状況一覧<span>{{ checked_at }}</span></h1>
    <table>
      <thead>
        <tr>
          <th>#</th><th>##</th><th>ドメイン</th><th>FQDN</th><th>ステータス</th><th>期限終了日時</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="(data, brand, pidx) in list">
          <tr v-for="(result, fqdn, sidx) in data" v-bind:class="{ 'odd' : pidx%2 !== 0 }">
            <td>{{ pidx+1 }}</td>
            <td>{{ sidx+1 }}</td>
            <td>{{ brand }}</td>
            <td>{{ fqdn }}</td>
            <td v-if="result.status">
              <span v-if="result.status === 1" class="ok">正常</span><span v-if="result.status === 2" class="note">間近</span><span v-if="result.status === 3" class="note">間近！</span><span v-if="result.status === 4" class="ng">失効</span><span v-if="result.status === 5" class="error">失敗</span>
            </td><td v-else>-</td>
            <td v-if="result.limit_at">{{ result.limit_at }}</td><td v-else>-</td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'Ssl',
  data: function(){
    return { 
        list:{},
        checked_at:null,
        is_error:false
    }
  },
  mounted:function() {
    window.addEventListener('DOMContentLoaded', this.getList)
  },
  methods: {
    getList:function(){
      document.body.classList.add('loading')
      this.$axios.get('https://ssl-check.ketoha.xyz/api/').then(function(response){
        this.list = {}
        this.checked_at = response.data.checked_at
        let list = response.data.list
//console.log(list)
        for (let brand in list) {
          this.list[brand] = {}
          for (let fqdn in list[brand]) {
            this.list[brand][fqdn] = JSON.parse(list[brand][fqdn])
          }
        }
      }.bind(this)).catch(function(error){
        this.is_error = true
      }.bind(this)).finally(function(){
        document.body.classList.remove('loading')
      }.bind(this)
    )}
  }
}
</script>

<style scoped>

</style>
