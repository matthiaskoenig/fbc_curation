<template>
    <div class="p-p-4">

        <h1 v-if="running">Running FROG</h1>
        <h1 v-else>FROG Report</h1>
        <h2>{{ $route.params.id }}</h2>
        <span v-if="running">Please be patient. Running a complete FROG analysis for large models
        can take some time. You can check back later for your results using the url
        <code>{{ report_url }}</code>.

        </span>
        <ProgressBar v-if="running" class="p-my-5" mode="indeterminate" style="height: 0.5em;"/>
        <Tag :value="status" :severity="tag_class"></Tag><br />
        <code class="error">{{ error }}</code>
        <span v-if="success">
            Download COMBINE archive with FROG Report <br/>
            <a :href="omex_url" title="Download FROG COMBINE archive"><img v-if="success"
                            src="@/assets/images/archive.png"
                            width="200"
                        /></a>
        </span>



        <div>
            <code style="font-size: x-small">{{ result }}</code>
        </div>
    </div>
</template>

<script lang="ts">
import store, {VUE_APP_APIURL, VUE_APP_FRONTENDURL} from "@/store/index";
import { defineComponent } from "vue";
import axios from "axios";
import Tag from "primevue/tag";


export default defineComponent({
    components: {},
    data() {
        return {
            error: null,
            result: {
                manifest: null,
                frogs: null,
            },
            status: "UNDEFINED",
            status_color: "darkgray",
        };
    },
    computed: {
        task_id(){
            return this.$route.params.id;
        },
        running(){
            if (this.status == "PENDING"){
                return true;
            } else {
                return false;
            }
        },
        success(){
            if (this.status == "SUCCESS"){
                return true;
            } else {
                return false;
            }
        },
        omex_url(): string {
            return VUE_APP_APIURL + "/api/task/omex/" + this.task_id;
        },
        report_url(): string {
            return VUE_APP_FRONTENDURL + "/frog/" + this.task_id;
        },
        tag_class(){
             if (this.status == "PENDING"){
                 return "info";
             } else if (this.status == "SUCCESS"){
                 return "success";
             } else if (this.status == "FAILURE"){
                 return "danger";
             } else if (this.status == "ERROR"){
                 return "danger";
             } else {
                 return "info";
             }
        }
    },
    methods: {
        queryTaskStatus() {
            const url = VUE_APP_APIURL + "/api/task/status/" + this.task_id;
            console.log(url)
            axios.get(url)
                .then((res) => {
                    console.log(res);
                    this.status = res.data.task_status;
                    this.result = res.data.task_result;
                    if (this.status == "SUCCESS"){
                        return null;
                    } else if (this.status == "FAILURE"){
                        return null;
                    }
                })
                .catch((error) => {
                    console.log(error);
                    this.error = error;
                    this.status = "ERROR";
                    return null;
                });


            setTimeout(() => {
              this.queryTaskStatus();
            }, 2000);
        },
    },
    mounted() {
        this.queryTaskStatus();
  }
});
</script>

<style lang="scss">
.success {
    color: green;
}
.failure {
    color: red;
}
.error {
    color: darkred;
}
.pending {
    color: blue;
}

#pot {
  //bottom: 15%;
    //top: 6.5em;

  position: relative;
  -webkit-animation: linear infinite;
  -webkit-animation-name: run;
  -webkit-animation-duration: 10s;
    backface-visibility: hidden;
}
@-webkit-keyframes run {
    0% { left: 0;}
    50%{ left : calc(100% - 40px);}
    100%{ left: 0;}
}
</style>
