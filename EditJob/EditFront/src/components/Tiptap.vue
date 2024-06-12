<template>
    <editor-content :editor="editor" />
</template>

<script setup>
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'

// useEditor方法创建了一个编辑器实例
// extensions 属性是一个数组，用于指定要加载的编辑器扩展。
// 在这里，只加载了 StarterKit 扩展，该扩展提供了一些基础的编辑功能，如粗体、斜体、段落等。
const editor = useEditor({
  content: '<p>I’m running Tiptap with Vue.js. 🎉</p>',
  extensions: [
    StarterKit,
  ],
})
</script>