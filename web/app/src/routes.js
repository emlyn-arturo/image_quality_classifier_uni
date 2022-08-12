import VueRouter from 'vue-router'

import * as NotFound from './_Core/NotFound.vue'

import * as UnikittyPy from './UnikittyPy/Index.vue'
import * as Upload from './UnikittyPy/Upload.vue'

const routes = [
  {
    path: '/',
    component: UnikittyPy,
    children: [
      {
        path: '',  // Default route, parent should not be named
        component: Upload,
        name: 'image_upload'
      }
    ]
  },
  {
    path: '*',
    component: NotFound,
    name: 'not_found'
  }
];

export const router = new VueRouter({routes: routes, mode: 'history'});
