<template>
  <div class="hello">
   <body>
    <nav class="navbar navbar-default navbar-static-top">
        <div class="container-fluid">
            <ul class="nav navbar-nav navbar-left">
                <li><a href="#">Witaj xxx masz:xxxx punktów</a></li>
            </ul>
            <ul class="nav navbar-nav navbar-right">
                <li><a href="onet.pl">Targ</a></li>
                <li><a href="onet.pl">Dodaj</a></li>
                  <li><a href="onet.pl">Wyloguj</a></li>
                  <li><a href="onet.pl"">Zaloguj</a></li>

            </ul>
        </div>
    </nav>
    <div class="container-fluid">
    </div>


</body>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
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
  color: #42b983;
}
</style>
