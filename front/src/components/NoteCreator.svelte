<script lang="ts">
  import { noteApi } from '../lib/api';
  import ErrorDialog from './ErrorDialog.svelte';

  let content = $state('');
  let attachmentUrl = $state('');
  let attachmentType = $state('Image' as 'Image' | 'Video');
  let errorMessage = $state('');
  let isSubmitting = $state(false);

  async function handleSubmit() {
    if (!content) return;
    isSubmitting = true;
    errorMessage = '';
    try {
      const attachments = attachmentUrl ? [{ type: attachmentType, url: attachmentUrl, mime_type: attachmentType === 'Image' ? 'image/jpeg' : 'video/mp4' }] : undefined;
      await noteApi.create(content, attachments);
      content = '';
      attachmentUrl = '';
    } catch (e: any) {
      errorMessage = e.message || 'Failed to create note';
    } finally {
      isSubmitting = false;
    }
  }

  function handleRetry() {
    handleSubmit();
  }

  function handleCloseError() {
    errorMessage = '';
  }
</script>

<div class="card p-4 flex flex-col gap-3">
  <textarea 
    bind:value={content}
    placeholder="What's on your mind?"
    class="input w-full p-2 resize-none h-24"
    disabled={isSubmitting}
  ></textarea>
  
  <div class="flex gap-2">
    <input 
      bind:value={attachmentUrl}
      placeholder="Attachment URL (optional)"
      class="input flex-grow p-2"
      disabled={isSubmitting}
    />
    <select bind:value={attachmentType} class="input p-2" disabled={isSubmitting}>
      <option value="Image">Image</option>
      <option value="Video">Video</option>
    </select>
  </div>

  <button 
    onclick={handleSubmit}
    class="bg-gruvbox-blue text-gruvbox-light0 font-bold py-2 rounded-md hover:bg-opacity-80 transition-all disabled:opacity-50"
    disabled={isSubmitting || !content}
  >
    {isSubmitting ? 'Posting...' : 'Post Note'}
  </button>
</div>

{#if errorMessage}
  <ErrorDialog 
    message={errorMessage} 
    onRetry={handleRetry} 
    onClose={handleCloseError} 
  />
{/if}
