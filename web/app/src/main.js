import Vue from 'vue'
import VueRouter from 'vue-router'
import * as Layout from './_Core/Layout.vue'
import * as ErrorComponent from './_Core/Error.vue'
import {router} from './routes.js'

Vue.use(VueRouter);

Vue.component('tsno-error', ErrorComponent);

new Vue({
    router,
    el: '#app',
    render: h => h(Layout),
});
