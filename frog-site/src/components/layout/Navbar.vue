<template>
    <menubar :model="items">
        <template #start>
            <div class="p-d-flex">
                <router-link to="/">
                    <img
                        to="/"
                        alt="logo"
                        src="@/assets/images/frog-192x192.png"
                        height="35"
                    />
                </router-link>
                <router-link to="/">
                    <span class="frog p-mx-3" style="color: black"
                        >FROG</span
                    >
                </router-link>
            </div>
        </template>
    </menubar>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import store from "@/store";

/**
 * Navbar component for providing main links in the application
 */
export default defineComponent({
    data() {
        return {
            items: [
                {
                    label: "Home",
                    icon: "pi pi-fw pi-home",
                    to: "/",
                },
                {
                    label: "REST API",
                    icon: "pi pi-fw pi-sitemap",
                    url: "http://localhost:1555/docs",
                },
                // {
                //     label: "Examples",
                //     icon: "pi pi-fw pi-list",
                //     to: "/examples",
                // },
                // {
                //     label: "About",
                //     icon: "pi pi-fw pi-info-circle",
                //     to: "/about",
                // },

                {
                    label: "Report issue",
                    icon: "pi pi-fw pi-pencil",
                    url: "https://github.com/matthiaskoenig/fbc_curation/issues/new/choose",
                },
                {
                    label: "Source",
                    icon: "pi pi-fw pi-github",
                    url: "https://github.com/matthiaskoenig/fbc_curation",
                },
            ],
        };
    },
});
</script>

<style lang="scss" scoped>
.frog {
    font-family: "Roboto Slab", serif;
    font-size: 30px;
}
</style>
