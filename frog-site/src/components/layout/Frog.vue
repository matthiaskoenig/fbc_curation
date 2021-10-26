<template>
    <div class="p-p-4">
    <ProgressBar v-if="running" class="p-my-5" mode="indeterminate" style="height: 0.5em" />
    <h1>FROG report</h1>
    <h2>{{ $route.params.id }}</h2>


    <strong>Status</strong>: <Tag :value="status"></Tag>
        <div>
            <code style="font-size: x-small">{{ result }}</code>
        </div>
    </div>
</template>

<script lang="ts">
import store, {VUE_APP_APIURL} from "@/store/index";
import { defineComponent } from "vue";
import axios from "axios";
import Tag from "primevue/tag";


export default defineComponent({
    components: {},

    computed: {
        task_id(){
            return this.$route.params.id;
        }
    },
    data() {
        return {
            response: {},
            status: "-",
            result: null,
            running: true,
        };
    },
    methods: {
        queryTaskStatus() {
            this.running = true
            const url = VUE_APP_APIURL + "/tasks/" + this.task_id;
            console.log(url)
            axios.get(url)
                .then((res) => {
                    console.log(res);
                    this.status = res.data.task_status;
                    this.result = res.data.task_result;
                    this.response = res
                })
                .catch((error) => {
                    console.log(error);
                });
            if (this.status === "SUCCESS"){
                this.running = false

                return null;
            }

            setTimeout(() => {
              this.queryTaskStatus();
            }, 1000);
        },
    },
    mounted() {
        this.queryTaskStatus();
  }
});
</script>

<style lang="scss">
</style>
