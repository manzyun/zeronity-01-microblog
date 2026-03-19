<script lang="ts">
  import { noteApi } from '../lib/api';
  import { formatDistanceToNow } from 'date-fns';

  let { note, onDeleted } = $props<{
    note: {
      id: string;
      content: string;
      published: string;
      author?: {
        username: string;
        preferred_username: string;
      };
      attachments?: Array<{
        type: 'Image' | 'Video';
        url: string;
        mime_type: string;
      }>;
    };
    onDeleted?: () => void;
  }>();

  async function handleDelete() {
    if (!confirm('Are you sure you want to delete this note?')) return;
    try {
      await noteApi.delete(note.id);
      onDeleted?.();
    } catch (e: any) {
      alert(e.message || 'Failed to delete note');
    }
  }

  const publishedDate = new Date(note.published);
</script>

<div class="card overflow-hidden mb-6 max-w-lg mx-auto">
  <!-- Header -->
  <div class="p-4 flex items-center gap-3 border-b border-gruvbox-dark2">
    <div class="w-10 h-10 rounded-full bg-gruvbox-dark3 flex items-center justify-center font-bold text-gruvbox-light0">
      {note.author?.username?.[0].toUpperCase() || '?'}
    </div>
    <div class="flex-grow">
      <div class="font-bold text-gruvbox-light0">{note.author?.preferred_username || note.author?.username || 'Unknown User'}</div>
      <div class="text-xs text-gruvbox-light4">@{note.author?.username || 'unknown'}</div>
    </div>
    <button onclick={handleDelete} class="text-gruvbox-red hover:text-opacity-80 transition-all text-sm">
      Delete
    </button>
  </div>

  <!-- Content -->
  <div class="p-4 text-gruvbox-light1 whitespace-pre-wrap">
    {note.content}
  </div>

  <!-- Attachments -->
  {#if note.attachments && note.attachments.length > 0}
    <div class="border-t border-gruvbox-dark2 bg-black/20">
      {#each note.attachments as attachment}
        {#if attachment.type === 'Image'}
          <img src={attachment.url} alt="Note attachment" class="w-full h-auto block" />
        {:else if attachment.type === 'Video'}
          <video src={attachment.url} controls class="w-full h-auto block">
            <track kind="captions" />
          </video>
        {/if}
      {/each}
    </div>
  {/if}

  <!-- Footer -->
  <div class="p-4 border-t border-gruvbox-dark2 flex justify-between items-center text-xs text-gruvbox-light4">
    <div>{formatDistanceToNow(publishedDate, { addSuffix: true })}</div>
    <div class="flex gap-4">
      <button class="hover:text-gruvbox-light1 transition-colors">Like</button>
      <button class="hover:text-gruvbox-light1 transition-colors">Reply</button>
    </div>
  </div>
</div>
