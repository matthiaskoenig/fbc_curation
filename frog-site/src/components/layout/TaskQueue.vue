<template>
    <div>
        <h1>Task Queue</h1>
        Task Id: {{ task_id }}<br />
        Status: {{ status }}<br />
        <Button class="p-mt-2" type="button" @click="submitTask($event)"
            >Submit Task</Button>
        <Button class="p-mt-2" type="button" @click="queryTaskStatus($event)"
            >Query Status</Button>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { FilterMatchMode, FilterOperator } from "primevue/api";
import store, { VUE_APP_APIURL } from "@/store";
import axios from "axios";
import { checkAPIResponse } from "@/helpers/additionalInfoUtils";

export default defineComponent({
    name: "TaskQueue",
    data() {
        return {
            task_id: "-",
            status: "-",
        };
    },
    methods: {
        submitTask() {
            const url = "http://0.0.0.0:1556/api" + "/tasks/";
            //const response = await axios.get(url);
            axios
                .post(url,
                    {
                        type: 1,
                    },
                )
                .then((res) => {
                    console.log(res);
                    this.task_id = res.data.task_id;
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        queryTaskStatus() {
            const url = "http://0.0.0.0:1556/api" + "/tasks/" + this.task_id;
            //const response = await axios.get(url);
            axios.get(url)
                .then((res) => {
                    console.log(res);
                    this.status = res.data;
                })
                .catch((error) => {
                    console.log(error);
                });
        },
    },
});
</script>

<style lang="scss" scoped></style>
