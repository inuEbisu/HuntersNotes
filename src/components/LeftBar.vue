<script setup lang="ts">
import {
    nextTick,
    onBeforeUnmount,
    onMounted,
    ref,
    watch,
    watchEffect,
} from "vue";
import { render_list } from "@/assets/ts/leftbar";
import { LEFTBAR_STATUS } from "@/assets/ts/types";
import { OverlayScrollbarsComponent } from "overlayscrollbars-vue";
import hotkeys from "hotkeys-js";
import Search from "./Search.vue";

// Cache
import config from "@cache/config";

// Types
import type { Ref } from "vue";
import type { JSX } from "vue/jsx-runtime";
import type { HotkeysEvent } from "hotkeys-js";
import type { PartialOptions } from "overlayscrollbars";

const props = defineProps<{
    status: LEFTBAR_STATUS;
    currentCategory: string;
}>();

const osOptions: PartialOptions = {
    scrollbars: { autoHide: "move" },
    overflow: { x: "hidden" },
};

/** Attributes attached to a category */
interface Category {
    name: string;
    link: string;
    opacity: number;
    timeout?: NodeJS.Timeout;
}

/** Categories to be displayed as buttons. */
const categories: Ref<Category[]> = ref(
    config.nav.map((c) => ({
        name: c.title,
        link: c.link,
        opacity: 0,
    }))
);

/** ID of category of current page, -1 iff current location is index page. */
const category_id: number = categories.value.findIndex(
    (c) => c.link === "/" + props.currentCategory
);

/** ID of active category. */
const active_id: Ref<number> = ref(category_id === -1 ? 0 : category_id);

// This variable may be true only when status == HOVER_TO_SHOW.
const do_show_detail: Ref<boolean> = ref(false);
const is_searching: Ref<boolean> = ref(false);

const REVEAL_DELAY = 15;

const category = {
    reveal: () => {
        let len = categories.value.length;

        for (let i = 0; i < len; i++) {
            clearTimeout(categories.value[i].timeout);

            let timeout: NodeJS.Timeout = setTimeout(() => {
                categories.value[i].opacity = 1;
            }, REVEAL_DELAY * i);

            categories.value[i].timeout = timeout;
        }
    },
    hide: () => {
        let len = categories.value.length;

        for (let i = len - 1; i >= 0; i--) {
            clearTimeout(categories.value[i].timeout);

            let timeout: NodeJS.Timeout = setTimeout(() => {
                categories.value[i].opacity = 0;
            }, REVEAL_DELAY * (len - 1 - i));

            categories.value[i].timeout = timeout;
        }
    },
};

const search = {
    reveal: async () => {
        is_searching.value = true;
        await nextTick();

        const input = document.querySelector(".search .input") as any;
        input.focus();
    },
    hide: () => {
        is_searching.value = false;
    },
};

const mouse = {
    // Handle mouse events only if current status is HOVER_TO_SHOW
    enter: () => {
        if (props.status === LEFTBAR_STATUS.HOVER_TO_SHOW) {
            do_show_detail.value = true;
            category.reveal();
        }
    },
    leave: () => {
        if (props.status === LEFTBAR_STATUS.HOVER_TO_SHOW) {
            do_show_detail.value = false;
            category.hide();
        }
    },
    /** Switch category to `index` */
    switch: (index: number) => {
        active_id.value = index;
    },
};

const keyboard = {
    command_k: (event: KeyboardEvent, handler: HotkeysEvent) => {
        if (!is_searching.value) {
            search.reveal();
        }
    },

    esc: (event: KeyboardEvent, handler: HotkeysEvent) => {
        if (is_searching.value) {
            search.hide();
        }
    },
};

const VBody_fn = () => () => render_list(config.nav[active_id.value], true);
const VBody: Ref<() => JSX.Element> = ref(VBody_fn());
watch(active_id, () => (VBody.value = VBody_fn()));

onMounted(() => {
    hotkeys("command+k,ctrl+k", keyboard.command_k);
    hotkeys("esc", keyboard.esc);
});

onBeforeUnmount(() => {
    hotkeys.unbind("command+k,ctrl+k");
    hotkeys.unbind("esc");
});

watchEffect(() => {
    if (props.status === LEFTBAR_STATUS.SHOW_SEARCH_AND_CATEGORY) {
        category.reveal();
    }
});
</script>

<template>
    <div
        id="left"
        @mouseenter="mouse.enter"
        @mouseleave="mouse.leave"
        :style="{
            '--z-index': do_show_detail
                ? 1001
                : status == LEFTBAR_STATUS.HOVER_TO_SHOW
                ? 0
                : 1001,
            '--height':
                status == LEFTBAR_STATUS.HOVER_TO_SHOW
                    ? 'calc(100vh - var(--offset-top) * 2)'
                    : 'unset',
        }"
    >
        <ul class="nav">
            <li class="btn" id="search" @click="search.reveal">
                <font-awesome-icon :icon="['fas', 'magnifying-glass']" />
            </li>
        </ul>

        <div
            class="category"
            v-if="status != LEFTBAR_STATUS.ONLY_SEARCH_BUTTON"
        >
            <template v-for="(item, idx) in categories">
                <a
                    class="item"
                    :class="idx == active_id && 'active'"
                    :style="{ opacity: item.opacity }"
                    @click.prevent="$router.push(item.link)"
                    @mouseover="mouse.switch(idx)"
                    :href="item.link"
                >
                    {{ item.name }}
                </a>
            </template>
        </div>

        <OverlayScrollbarsComponent
            element="div"
            class="content-wrapper"
            :options="(osOptions as any)"
            defer
        >
            <Transition name="content">
                <component class="content" :is="VBody" v-if="do_show_detail" />
            </Transition>
        </OverlayScrollbarsComponent>

        <!-- https://cn.vuejs.org/guide/built-ins/teleport.html -->
        <Teleport to="body">
            <Transition name="search">
                <KeepAlive>
                    <Search v-if="is_searching" @close="search.hide" />
                </KeepAlive>
            </Transition>
        </Teleport>
    </div>
</template>

<style lang="stylus">
@import "../assets/css/global.styl";

// Nav
$nav-height = 40px;
$nav-hover-color = $theme-color;
$nav-hov-background-color = alpha($theme-color, 12%);

$item-active-color = $theme-color;
$item-underline-color = alpha($theme-color, 65%);
$item-hov-background-color = alpha($theme-color, 12%);

// TOC
$toc-translate-offset = -8px;
$toc-offset-left = 28px;
$toc-offset-top = 11px + $nav-height;
$toc-width = 240px;
$toc-title-height = 1.45rem;
$toc-title-indent = 0.5rem;

// Search
$search-scale = 0.99;

// Global
$background-radius = 4px;
$width = $toc-offset-left + $toc-width;

#left
    // Nav
    scheme(--nav-color, lighten($text-color, 45%), darken($text-color-d, 15%));
    scheme(--item-color, lighten($text-color, 10%), darken($text-color-d, 8%));
    dual(--nav-act-background-color, alpha($theme-color, 30%), unset);
    dual(--item-act-background-color, alpha($theme-color, 30%), unset);
    dual(--nav-width, 42px, 35px);
    dual(--nav-gap, 2px, 0px);

    // TOC
    scheme(--toc-color, lighten($text-color, 30%), darken($text-color-d, 5%));

    // Global
    scheme(--background-color, alpha($background-light, 90%), alpha($background-dark, 90%));
    dual(--offset-top, 28px, 32px);
    dual(--offset-left, 35px, 27px);

    position: fixed;
    left: var(--offset-left);
    top: var(--offset-top);
    width: $width;
    height: var(--height);
    z-index: var(--z-index);

    .nav, .category, .content
        background-color: var(--background-color);

    .nav
        display: flex;
        flex-direction: row;
        width: fit-content;
        gap: var(--nav-gap);

        .btn
            height: $nav-height;
            width: var(--nav-width);
            text-align: center;
            line-height: $nav-height;
            font-size: 1.2rem;
            border-radius: 3px;
            transition: background-color 0.07s, color 0.08s;
            color: var(--nav-color);
            cursor: pointer;
            display: block;

            &:hover
                background-color: $nav-hov-background-color;
                color: $nav-hover-color;

            &:active
                background-color: var(--nav-act-background-color);
                color: $nav-active-color;

    .category
        position: absolute;
        display: flex;
        flex-direction: row;
        top: 0;
        left: calc(var(--nav-width) + var(--nav-gap));
        height: $nav-height;
        text-wrap: nowrap;
        overflow: hidden;
        border-radius: $background-radius;
        user-select: none;

        .item
            height: $nav-height;
            line-height: $nav-height;
            font-size: 0.94rem;
            padding: 0 12px;
            color: var(--item-color);
            text-decoration-color: transparent;
            border-radius: 3px;
            transition: background-color 0.07s, opacity 0.08s, text-decoration-color 0.08s;

            &:hover
                color: $item-active-color;
                background-color: $item-hov-background-color;

            &:active
                color: $item-active-color;
                background-color: var(--item-act-background-color);

            &.active
                color: $item-active-color;
                text-decoration-line: underline;
                text-underline-offset: 5px;
                text-decoration-style: wavy;
                text-decoration-color: $item-underline-color;

    .content-wrapper
        position: absolute;
        left: $toc-offset-left;
        top: $toc-offset-top;
        width: $toc-width;
        bottom: 0;

        .content
            position: absolute;
            border-radius: $background-radius;
            padding: 15px 0;

            .title
                color: var(--toc-color);
                font-size: 0.95rem;
                line-height: $toc-title-height;
                margin-bottom: 5px;
                padding-right: 10px;
                display: flex;
                gap: 8px;
                transition: color 0.2s;

            .title.router-link-exact-active .text
                color: $theme-color;

            .title .sign
                color: $theme-color;
                opacity: 0;
                transition: opacity 0.1s;
                font-size: 0.7rem;
                display: block;
                animation: shake-x 1s infinite ease-in-out;

            .title .text
                text-indent: 0 - $toc-title-indent;
                padding-left: $toc-title-indent;

            .title:hover .text
                color: $theme-color;

            .title:hover .sign
                opacity: 1;

            .children
                margin-left: 1rem;

            &> .children
                margin: 0;

    .content-enter-active,
    .content-leave-active
        transition-property: opacity, transform;

    .content-enter-active
        transition-duration: 0.12s;
        transition-timing-function: ease-out;

    .content-leave-active
        transition-duration: 0.07s;
        transition-timing-function: cubic-bezier(0.15, 0.79, 0.69, 0.68);

    .content-enter-from,
    .content-leave-to
        opacity: 0;
        transform: translateY($toc-translate-offset);


.search-enter-active,
.search-leave-active
    transition-property: opacity, transform;
    transition-duration: 0.07s;

.search-enter-active
    transition-timing-function: cubic-bezier(0.41, 0.16, 0.83, 0.74);

.search-leave-active
    transition-timing-function: cubic-bezier(0.08, 0.46, 0.76, 0.89);

.search-enter-from,
.search-leave-to
    opacity: 0;
    transform: scale($search-scale);

@media only screen and (max-width: 748px)
    #left
        position: absolute;

        .nav .btn
            font-size: 1rem;

        .category .item
            font-size: 0.85rem;
            padding: 0 9px;
</style>
