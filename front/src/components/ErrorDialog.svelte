<script lang="ts">
  let { message, onRetry, onClose } = $props<{
    message: string;
    onRetry?: () => void;
    onClose: () => void;
  }>();
</script>

<div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
  <div class="card p-6 max-w-sm w-full mx-4 shadow-xl">
    <h2 class="text-gruvbox-red font-bold text-xl mb-4">Error</h2>
    <p class="text-gruvbox-light1 mb-6">{message}</p>
    <div class="flex justify-end gap-3">
      {#if onRetry}
        <button 
          onclick={onRetry}
          class="bg-gruvbox-blue text-gruvbox-light0 px-4 py-2 rounded hover:bg-opacity-80 transition-all"
        >
          再試行 (Retry)
        </button>
      {/if}
      <button 
        onclick={onClose}
        class="bg-gruvbox-dark2 text-gruvbox-light1 px-4 py-2 rounded hover:bg-opacity-80 transition-all"
      >
        閉じる (Close)
      </button>
    </div>
  </div>
</div>
