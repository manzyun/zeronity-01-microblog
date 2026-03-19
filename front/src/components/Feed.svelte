<script lang="ts">
  import { onMount } from 'svelte';
  import { noteApi } from '../lib/api';
  import Note from './Note.svelte';
  import NoteCreator from './NoteCreator.svelte';

  let notes = $state([] as any[]);
  let isLoading = $state(true);
  let error = $state('');

  async function fetchNotes() {
    isLoading = true;
    error = '';
    try {
      notes = await noteApi.list();
    } catch (e: any) {
      error = e.message || 'Failed to fetch notes';
    } finally {
      isLoading = false;
    }
  }

  onMount(() => {
    fetchNotes();
  });

  function handleNoteDeleted() {
    fetchNotes();
  }
</script>

<div class="max-w-lg mx-auto w-full px-4">
  <div class="mb-8">
    <NoteCreator />
  </div>

  {#if isLoading}
    <div class="flex justify-center p-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gruvbox-blue"></div>
    </div>
  {:else if error}
    <div class="card p-8 text-center text-gruvbox-red">
      <p>{error}</p>
      <button onclick={fetchNotes} class="mt-4 text-gruvbox-blue hover:underline">
        Try again
      </button>
    </div>
  {:else if notes.length === 0}
    <div class="card p-8 text-center text-gruvbox-light4">
      No notes yet. Be the first to post!
    </div>
  {:else}
    {#each notes as note (note.id)}
      <Note {note} onDeleted={handleNoteDeleted} />
    {/each}
  {/if}
</div>
