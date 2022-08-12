webpackJsonp([1],[
/* 0 */,
/* 1 */,
/* 2 */,
/* 3 */,
/* 4 */,
/* 5 */,
/* 6 */,
/* 7 */,
/* 8 */,
/* 9 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_vue_router__ = __webpack_require__(3);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__Core_NotFound_vue__ = __webpack_require__(44);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__Core_NotFound_vue___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_1__Core_NotFound_vue__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__UnikittyPy_Index_vue__ = __webpack_require__(42);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__UnikittyPy_Index_vue___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2__UnikittyPy_Index_vue__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__UnikittyPy_Upload_vue__ = __webpack_require__(43);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__UnikittyPy_Upload_vue___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_3__UnikittyPy_Upload_vue__);







const routes = [{
  path: '/',
  component: __WEBPACK_IMPORTED_MODULE_2__UnikittyPy_Index_vue__,
  children: [{
    path: '', // Default route, parent should not be named
    component: __WEBPACK_IMPORTED_MODULE_3__UnikittyPy_Upload_vue__,
    name: 'image_upload'
  }]
}, {
  path: '*',
  component: __WEBPACK_IMPORTED_MODULE_1__Core_NotFound_vue__,
  name: 'not_found'
}];

const router = new __WEBPACK_IMPORTED_MODULE_0_vue_router__["a" /* default */]({ routes: routes, mode: 'history' });
/* harmony export (immutable) */ __webpack_exports__["a"] = router;


/***/ }),
/* 10 */
/***/ (function(module, exports, __webpack_require__) {

function injectStyle (ssrContext) {
  __webpack_require__(39)
}
var Component = __webpack_require__(1)(
  /* script */
  __webpack_require__(32),
  /* template */
  __webpack_require__(49),
  /* styles */
  injectStyle,
  /* scopeId */
  "data-v-f6993f00",
  /* moduleIdentifier (server only) */
  null
)

module.exports = Component.exports


/***/ }),
/* 11 */
/***/ (function(module, exports, __webpack_require__) {

function injectStyle (ssrContext) {
  __webpack_require__(37)
  __webpack_require__(38)
}
var Component = __webpack_require__(1)(
  /* script */
  __webpack_require__(33),
  /* template */
  __webpack_require__(47),
  /* styles */
  injectStyle,
  /* scopeId */
  "data-v-71a0363c",
  /* moduleIdentifier (server only) */
  null
)

module.exports = Component.exports


/***/ }),
/* 12 */,
/* 13 */,
/* 14 */,
/* 15 */,
/* 16 */,
/* 17 */,
/* 18 */,
/* 19 */,
/* 20 */,
/* 21 */,
/* 22 */,
/* 23 */,
/* 24 */,
/* 25 */,
/* 26 */,
/* 27 */,
/* 28 */,
/* 29 */,
/* 30 */,
/* 31 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__http_common_js__ = __webpack_require__(34);
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//



/* harmony default export */ __webpack_exports__["default"] = ({
    data() {
        return {
            files: null,
            files_raw: [],
            result: [],
            http_error: false,
            hovering: false,
            saving: false,
            failure: false,
            images: []
        };
    },
    methods: {
        feedback(label, filename) {
            this.saving = true;
            __WEBPACK_IMPORTED_MODULE_0__http_common_js__["a" /* HTTP */].post('api/feedback', {
                image: filename,
                feedback: label
            }).then(res => {
                for (let i = 0; i < this.result.length; ++i) {
                    let r = this.result[i];
                    if (this.result[i].file == filename) {
                        this.result[i].selected = label;
                        break;
                    }
                }
                this.saving = false;
            }).catch(err => {
                console.error(err);
                this.http_error = 'Fehler beim Senden des Feedback. ' + err;
                this.failure = true;
                this.saving = false;
            });
        },
        files_change(e) {
            let fileList = [];
            for (let f = 0; f < e.target.files.length; ++f) {
                fileList.push(e.target.files[f]);
            }
            console.log(fileList);
            let formData = new FormData();
            if (!fileList.length) return;
            this.files_raw = [];
            this.images = [];
            Array.from(Array(fileList.length).keys()).map(x => {
                let file = fileList[x];
                let fr = new FileReader();
                fr.onload = function () {
                    this.files_raw.push({
                        "filename": fileList[x].name,
                        "filedata": fr.result
                    });
                }.bind(this);
                fr.readAsDataURL(file);

                formData.append("image", fileList[x], fileList[x].name);
            });
            this.files = formData;
            this.upload_file(e);
            e.target.files = null;
            e.target.value = "";
            this.failure = false;
        },
        click_cirlce(e) {
            e.currentTarget.getElementsByTagName("input")[0].click();
        },
        upload_file(e) {
            this.saving = true;

            if (FileReader && this.files_raw && this.files_raw.length) {
                for (let i = 0; i < this.files_raw.length; ++i) {
                    let file = this.files_raw[i];
                    let fr = new FileReader();
                    fr.onload = function () {
                        this.images.push(fr.result);
                    }.bind(this);
                    fr.readAsDataURL(file);
                }
            }

            __WEBPACK_IMPORTED_MODULE_0__http_common_js__["a" /* HTTP */].post('api/evaluate', this.files).then(res => {
                e.target.blur();
                for (let i = 0; i < res.data.length; ++i) this.result.push(res.data[i]);
                this.file = null;
                this.saving = false;
                this.files_raw = [];
                // todo: stop spinner
            }).catch(err => {
                console.error(err);
                this.http_error = 'Fehler beim Bildupload. ' + err;
                this.failure = true;
                this.saving = false;
            });
        }
    }
});

/***/ }),
/* 32 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
//
//
//
//
//
//
//
//

/* harmony default export */ __webpack_exports__["default"] = ({
    props: ['message']
});

/***/ }),
/* 33 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
//
//
//
//
//
//
//

/* harmony default export */ __webpack_exports__["default"] = ({
    name: "home"
});

/***/ }),
/* 34 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_axios__ = __webpack_require__(13);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_axios___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_axios__);


const HTTP = __WEBPACK_IMPORTED_MODULE_0_axios___default.a.create({
    baseURL: '/'
    // baseURL: "http://localhost:5000/"
});
/* harmony export (immutable) */ __webpack_exports__["a"] = HTTP;


/***/ }),
/* 35 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_vue__ = __webpack_require__(12);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_vue_router__ = __webpack_require__(3);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__Core_Layout_vue__ = __webpack_require__(11);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__Core_Layout_vue___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2__Core_Layout_vue__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__Core_Error_vue__ = __webpack_require__(10);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__Core_Error_vue___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_3__Core_Error_vue__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__routes_js__ = __webpack_require__(9);






__WEBPACK_IMPORTED_MODULE_0_vue__["a" /* default */].use(__WEBPACK_IMPORTED_MODULE_1_vue_router__["a" /* default */]);

__WEBPACK_IMPORTED_MODULE_0_vue__["a" /* default */].component('tsno-error', __WEBPACK_IMPORTED_MODULE_3__Core_Error_vue__);

new __WEBPACK_IMPORTED_MODULE_0_vue__["a" /* default */]({
    router: __WEBPACK_IMPORTED_MODULE_4__routes_js__["a" /* router */],
    el: '#app',
    render: h => h(__WEBPACK_IMPORTED_MODULE_2__Core_Layout_vue__)
});

/***/ }),
/* 36 */
/***/ (function(module, exports) {

// removed by extract-text-webpack-plugin

/***/ }),
/* 37 */
/***/ (function(module, exports) {

// removed by extract-text-webpack-plugin

/***/ }),
/* 38 */
/***/ (function(module, exports) {

// removed by extract-text-webpack-plugin

/***/ }),
/* 39 */
/***/ (function(module, exports) {

// removed by extract-text-webpack-plugin

/***/ }),
/* 40 */,
/* 41 */,
/* 42 */
/***/ (function(module, exports, __webpack_require__) {

var Component = __webpack_require__(1)(
  /* script */
  null,
  /* template */
  __webpack_require__(46),
  /* styles */
  null,
  /* scopeId */
  null,
  /* moduleIdentifier (server only) */
  null
)

module.exports = Component.exports


/***/ }),
/* 43 */
/***/ (function(module, exports, __webpack_require__) {

function injectStyle (ssrContext) {
  __webpack_require__(36)
}
var Component = __webpack_require__(1)(
  /* script */
  __webpack_require__(31),
  /* template */
  __webpack_require__(45),
  /* styles */
  injectStyle,
  /* scopeId */
  "data-v-29ca6025",
  /* moduleIdentifier (server only) */
  null
)

module.exports = Component.exports


/***/ }),
/* 44 */
/***/ (function(module, exports, __webpack_require__) {

var Component = __webpack_require__(1)(
  /* script */
  null,
  /* template */
  __webpack_require__(48),
  /* styles */
  null,
  /* scopeId */
  null,
  /* moduleIdentifier (server only) */
  null
)

module.exports = Component.exports


/***/ }),
/* 45 */
/***/ (function(module, exports) {

module.exports={render:function (){var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;
  return _c('div', [_vm._m(0), _vm._v(" "), _c('tsno-error', {
    attrs: {
      "message": _vm.http_error
    }
  }), _vm._v(" "), _c('div', {
    staticClass: "circle-promoted dropzone",
    class: {
      'hovered': _vm.hovering, 'saving': _vm.saving, 'failure': _vm.failure
    },
    on: {
      "drop": function($event) {
        _vm.hovering = false
      },
      "dragenter": function($event) {
        _vm.hovering = true
      },
      "dragleave": function($event) {
        _vm.hovering = false
      }
    }
  }, [_c('svg', {
    staticStyle: {
      "fill-rule": "evenodd",
      "clip-rule": "evenodd",
      "stroke-linejoin": "round",
      "stroke-miterlimit": "1.41421"
    },
    attrs: {
      "width": "100%",
      "height": "100%",
      "viewBox": "0 0 152 152",
      "version": "1.1",
      "xmlns": "http://www.w3.org/2000/svg",
      "xmlns:xlink": "http://www.w3.org/1999/xlink",
      "xml:space": "preserve"
    }
  }, [_c('g', {
    attrs: {
      "id": "Group"
    }
  }, [_c('g', [_c('path', {
    staticStyle: {
      "fill": "url(#_Radial1)"
    },
    attrs: {
      "d": "M152.009,75.969c0,-41.929 -34.04,-75.969 -75.969,-75.969c-41.928,0 -75.968,34.04 -75.968,75.969c0,41.928 34.04,75.968 75.968,75.968c41.929,0 75.969,-34.04 75.969,-75.968Z"
    }
  }), _c('clipPath', {
    attrs: {
      "id": "_clip2"
    }
  }, [_c('path', {
    attrs: {
      "d": "M152.009,75.969c0,-41.929 -34.04,-75.969 -75.969,-75.969c-41.928,0 -75.968,34.04 -75.968,75.969c0,41.928 34.04,75.968 75.968,75.968c41.929,0 75.969,-34.04 75.969,-75.968Z"
    }
  })]), _c('g', {
    attrs: {
      "clip-path": "url(#_clip2)"
    }
  }, [_c('g', [_c('path', {
    staticStyle: {
      "fill": "url(#_Linear3)"
    },
    attrs: {
      "d": "M47.265,54.038l35.169,1.25l16.029,-5.826l6.47,6.47l6.71,-6.709l62.778,62.778l-51.642,51.642l-6.47,-6.47l-13.631,13.631l-62.778,-62.778l8.404,-22.151l-1.039,-31.837Z"
    }
  })])])]), _c('g', [_c('path', {
    staticStyle: {
      "fill": "#fff",
      "fill-rule": "nonzero"
    },
    attrs: {
      "d": "M72.199,84.315l-5.34,-5.34l-1.819,1.806l7.159,7.159l15.367,-15.368l-1.806,-1.805l-13.561,13.548Z"
    }
  }), _c('path', {
    staticStyle: {
      "fill": "#fff",
      "fill-rule": "nonzero"
    },
    attrs: {
      "d": "M64.386,40.006l-7.109,7.769l-12.315,0c-4.273,0 -7.769,3.496 -7.769,7.77l0,46.617c0,4.273 3.496,7.77 7.769,7.77l62.157,0c4.273,0 7.769,-3.497 7.769,-7.77l0,-46.617c0,-4.274 -3.496,-7.77 -7.769,-7.77l-12.315,0l-7.109,-7.769l-23.309,0Zm11.654,58.271c-10.722,0 -19.423,-8.702 -19.423,-19.424c0,-10.722 8.701,-19.424 19.423,-19.424c10.722,0 19.424,8.702 19.424,19.424c0,10.722 -8.702,19.424 -19.424,19.424Z"
    }
  })])]), _c('defs', [_c('radialGradient', {
    attrs: {
      "id": "_Radial1",
      "cx": "0",
      "cy": "0",
      "r": "1",
      "gradientUnits": "userSpaceOnUse",
      "gradientTransform": "matrix(196.073,-196.073,121.471,121.471,24.1918,27.3371)"
    }
  }, [_c('stop', {
    staticStyle: {
      "stop-color": "#0cc300",
      "stop-opacity": "1"
    },
    attrs: {
      "offset": "0"
    }
  }), _c('stop', {
    staticStyle: {
      "stop-color": "#0d420c",
      "stop-opacity": "1"
    },
    attrs: {
      "offset": "1"
    }
  })], 1), _c('linearGradient', {
    attrs: {
      "id": "_Linear3",
      "x1": "0",
      "y1": "0",
      "x2": "1",
      "y2": "0",
      "gradientUnits": "userSpaceOnUse",
      "gradientTransform": "matrix(-90.5293,-89.8876,98.9622,-82.2279,148.851,145.18)"
    }
  }, [_c('stop', {
    staticStyle: {
      "stop-color": "#000",
      "stop-opacity": "0"
    },
    attrs: {
      "offset": "0"
    }
  }), _c('stop', {
    staticStyle: {
      "stop-color": "#000",
      "stop-opacity": "0.364706"
    },
    attrs: {
      "offset": "1"
    }
  })], 1)], 1)]), _vm._v(" "), _c('input', {
    attrs: {
      "multiple": "",
      "type": "file"
    },
    on: {
      "drop": _vm.files_change,
      "change": _vm.files_change
    }
  })]), _vm._v(" "), _c('h2', [_vm._v("UnikittyPy")]), _vm._v(" "), _c('div', {
    staticClass: "results"
  }, [_vm._l((_vm.files_raw), function(image) {
    return _c('div', {
      staticClass: "circle-promoted dropzone",
      class: {
        'hovered': _vm.hovering, 'saving': _vm.saving, 'failure': _vm.failure
      },
      style: ({
        backgroundImage: 'url(' + image.filedata + ')'
      })
    })
  }), _vm._v(" "), _vm._l((_vm.result), function(res) {
    return _c('div', {
      staticClass: "circle-promoted dropzone",
      class: {
        'failure': res.result == 0,
          'success': res.result == 1, 'not-selected': !res.hasOwnProperty('selected')
      },
      style: ({
        backgroundImage: 'url(/uploads/' + res.file + ')'
      })
    }, [(!res.hasOwnProperty('selected')) ? _c('div', {
      staticClass: "controls"
    }, [_c('div', {
      staticClass: "success not-selected",
      on: {
        "click": function($event) {
          _vm.feedback(1, res.file)
        }
      }
    }, [_vm._v("OK")]), _vm._v(" "), _c('div', {
      staticClass: "failure not-selected",
      on: {
        "click": function($event) {
          _vm.feedback(0, res.file)
        }
      }
    }, [_vm._v("X")])]) : _c('div', {
      staticClass: "controls"
    }, [(res.hasOwnProperty('selected') && res.selected == 1) ? _c('div', {
      staticClass: "success"
    }, [_vm._v("OK")]) : (res.hasOwnProperty('selected') && res.selected == 0) ? _c('div', {
      staticClass: "failure"
    }, [_vm._v("X")]) : _vm._e()])])
  })], 2), _vm._v(" "), _c('a', {
    attrs: {
      "href": "http://localhost:5000/api/train",
      "target": "_blank"
    }
  }, [_vm._v("Train")])], 1)
},staticRenderFns: [function (){var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;
  return _c('p', [_vm._v("\n        Lade eines oder mehrere Bilder hoch und "), _c('br'), _vm._v("\n        lass es dir von unserem Netzwerk bewerten!\n    ")])
}]}

/***/ }),
/* 46 */
/***/ (function(module, exports) {

module.exports={render:function (){var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;
  return _c('div', [_c('router-view')], 1)
},staticRenderFns: []}

/***/ }),
/* 47 */
/***/ (function(module, exports) {

module.exports={render:function (){var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;
  return _c('div', {
    attrs: {
      "id": "app"
    }
  }, [_c('router-view', {
    staticClass: "main"
  })], 1)
},staticRenderFns: []}

/***/ }),
/* 48 */
/***/ (function(module, exports) {

module.exports={render:function (){var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;
  return _c('div', {
    attrs: {
      "id": "app"
    }
  }, [_vm._v("\n    Seite nicht gefunden.\n")])
},staticRenderFns: []}

/***/ }),
/* 49 */
/***/ (function(module, exports) {

module.exports={render:function (){var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;
  return (_vm.message) ? _c('div', {
    staticClass: "tsno-error"
  }, [_vm._m(0), _vm._v("\n    " + _vm._s(_vm.message) + "\n")]) : _vm._e()
},staticRenderFns: [function (){var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;
  return _c('p', [_c('strong', [_vm._v("Ein Fehler ist aufgetreten!")])])
}]}

/***/ })
],[35]);
//# sourceMappingURL=app.d6fe272180027aecf54b.js.map