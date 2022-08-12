<template>
    <div>
        <p>
            Lade eines oder mehrere Bilder hoch und <br>
            lass es dir von unserem Netzwerk bewerten!
        </p>

        <tsno-error :message="http_error"></tsno-error>

        <div class="circle-promoted dropzone"
             @drop="hovering=false"
             @dragenter="hovering=true"
             @dragleave="hovering=false"
             :class="{'hovered':hovering, 'saving':saving, 'failure':failure}">
            <svg width="100%" height="100%" viewBox="0 0 152 152" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
        <g id="Group"><g><path d="M152.009,75.969c0,-41.929 -34.04,-75.969 -75.969,-75.969c-41.928,0 -75.968,34.04 -75.968,75.969c0,41.928 34.04,75.968 75.968,75.968c41.929,0 75.969,-34.04 75.969,-75.968Z" style="fill:url(#_Radial1);"/><clipPath id="_clip2"><path d="M152.009,75.969c0,-41.929 -34.04,-75.969 -75.969,-75.969c-41.928,0 -75.968,34.04 -75.968,75.969c0,41.928 34.04,75.968 75.968,75.968c41.929,0 75.969,-34.04 75.969,-75.968Z"/></clipPath><g clip-path="url(#_clip2)"><g><path d="M47.265,54.038l35.169,1.25l16.029,-5.826l6.47,6.47l6.71,-6.709l62.778,62.778l-51.642,51.642l-6.47,-6.47l-13.631,13.631l-62.778,-62.778l8.404,-22.151l-1.039,-31.837Z" style="fill:url(#_Linear3);"/></g></g></g><g><path d="M72.199,84.315l-5.34,-5.34l-1.819,1.806l7.159,7.159l15.367,-15.368l-1.806,-1.805l-13.561,13.548Z" style="fill:#fff;fill-rule:nonzero;"/><path d="M64.386,40.006l-7.109,7.769l-12.315,0c-4.273,0 -7.769,3.496 -7.769,7.77l0,46.617c0,4.273 3.496,7.77 7.769,7.77l62.157,0c4.273,0 7.769,-3.497 7.769,-7.77l0,-46.617c0,-4.274 -3.496,-7.77 -7.769,-7.77l-12.315,0l-7.109,-7.769l-23.309,0Zm11.654,58.271c-10.722,0 -19.423,-8.702 -19.423,-19.424c0,-10.722 8.701,-19.424 19.423,-19.424c10.722,0 19.424,8.702 19.424,19.424c0,10.722 -8.702,19.424 -19.424,19.424Z" style="fill:#fff;fill-rule:nonzero;"/></g></g><defs><radialGradient id="_Radial1" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="matrix(196.073,-196.073,121.471,121.471,24.1918,27.3371)"><stop offset="0" style="stop-color:#0cc300;stop-opacity:1"/><stop offset="1" style="stop-color:#0d420c;stop-opacity:1"/></radialGradient><linearGradient id="_Linear3" x1="0" y1="0" x2="1" y2="0" gradientUnits="userSpaceOnUse" gradientTransform="matrix(-90.5293,-89.8876,98.9622,-82.2279,148.851,145.18)"><stop offset="0" style="stop-color:#000;stop-opacity:0"/><stop offset="1" style="stop-color:#000;stop-opacity:0.364706"/></linearGradient></defs>
      </svg>
            <input multiple type="file" @drop="files_change" @change="files_change">
        </div>

        <h2>UnikittyPy</h2>

        <div class="results">

            <div v-for="image in files_raw" class="circle-promoted dropzone"
                 :class="{'hovered':hovering, 'saving':saving, 'failure':failure}"
                 :style="{backgroundImage: 'url(' + image.filedata + ')'}">
            </div>
            <div v-for="res in result" class="circle-promoted dropzone"
             :class="{'failure': res.result == 0,
             'success': res.result == 1, 'not-selected': !res.hasOwnProperty('selected')}"
             :style="{backgroundImage: 'url(/uploads/' + res.file + ')'}">
                <div v-if="!res.hasOwnProperty('selected')" class="controls">
                    <div class="success not-selected" @click="feedback(1, res.file)">OK</div>
                    <div class="failure not-selected" @click="feedback(0, res.file)">X</div>
                </div>
                <div v-else="" class="controls">
                    <div v-if="res.hasOwnProperty('selected') && res.selected == 1" class="success">OK</div>
                    <div v-else-if="res.hasOwnProperty('selected') && res.selected == 0" class="failure">X</div>
                </div>
            </div>
        </div>

        <a href="http://localhost:5000/api/train" target="_blank">Train</a>

    </div>
</template>


<style scoped lang="sass" rel="stylesheet/sass">
    .dropzone.hovered:after
        border-color: #0065BD

    .results
        margin: 0 auto
        display: flex
        flex-wrap: wrap
        justify-content: center

        .dropzone:hover .controls
            opacity: 1
            margin-top: 0

        .controls
            opacity: 0
            margin-top: -20px
            position: absolute
            left: 0
            top: 0
            right: 0
            bottom: 0
            display: flex
            flex-wrap: wrap
            justify-content: space-around
            align-items: center
            transition: opacity 200ms ease-in-out, margin-top 200ms ease-in-out

            > div
                width: 10vmin
                height: 10vmin
                border-radius: 100%
                color: white
                display: flex
                justify-content: center
                align-items: center

                &.success
                    background: #2e7d32

                    &.not-selected
                        font-weight: bold
                        color: #2e7d32
                        background: rgba(255,255,255,0.46)

                        &:hover
                            background: rgba(255,255,255,0.8)

                &.failure
                    background: #c11900

                    &.not-selected
                        font-weight: bold
                        color: #c11900
                        background: rgba(255,255,255,0.46)

                        &:hover
                            background: rgba(255,255,255,0.8)

        .dropzone
            display: inline-block
            margin: 4vmin
            width: 32vmin
            height: 32vmin

    @keyframes rotating
      from
        transform: rotate(0deg)

      to
        transform: rotate(360deg)


    .saving:after
        border-style: dashed
        border-color: #0065BD
        animation: rotating 4s linear infinite


    .failure:after
        border-style: solid
        border-color: #c11900


    .success:after
        border-style: solid
        border-color: #2e7d32

    input[type=file]
        opacity: 0
        width: 100%
        height: 100%
        position: absolute
        top: 0
        left: 0
</style>


<script>
    import {HTTP} from '@/http-common.js'

    export default {
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
            }
        },
        methods: {
            feedback(label, filename) {
                this.saving = true;
                HTTP.post('api/feedback', {
                    image: filename,
                    feedback: label
                })
                    .then(res => {
                        for (let i = 0; i < this.result.length; ++i) {
                            let r = this.result[i];
                            if (this.result[i].file == filename) {
                                this.result[i].selected = label;
                                break;
                            }
                        }
                        this.saving = false;
                    })
                    .catch(err => {
                        console.error(err);
                        this.http_error = 'Fehler beim Senden des Feedback. '
                            + err;
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
                Array
                    .from(Array(fileList.length).keys())
                    .map(x => {
                        let file = fileList[x];
                        let fr = new FileReader();
                        fr.onload = function () {
                            this.files_raw.push({
                                "filename": fileList[x].name,
                                "filedata": fr.result
                            });
                        }.bind(this);
                        fr.readAsDataURL(file);

                        formData.append("image", fileList[x], fileList[x].name)
                    });
                this.files = formData;
                this.upload_file(e);
                e.target.files = null;
                e.target.value = "";
                this.failure = false;
            },
            click_cirlce(e) {
                e.currentTarget.getElementsByTagName("input")[0].click()
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

                HTTP.post('api/evaluate', this.files)
                    .then(res => {
                        e.target.blur();
                        for (let i = 0; i < res.data.length; ++i)
                            this.result.push(res.data[i]);
                        this.file = null;
                        this.saving = false;
                        this.files_raw = [];
                        // todo: stop spinner
                    })
                    .catch(err => {
                        console.error(err);
                        this.http_error = 'Fehler beim Bildupload. ' + err;
                        this.failure = true;
                        this.saving = false;
                    });
            }
        }
    }
</script>
