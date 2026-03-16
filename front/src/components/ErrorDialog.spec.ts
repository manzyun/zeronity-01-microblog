import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/svelte';
import ErrorDialog from './ErrorDialog.svelte';

describe('ErrorDialog Component', () => {
  it('should render the error message', () => {
    render(ErrorDialog, { message: 'Failed to fetch', onClose: vi.fn() });
    expect(screen.getByText('Failed to fetch')).toBeInTheDocument();
  });

  it('should call onClose when close button is clicked', async () => {
    const onClose = vi.fn();
    render(ErrorDialog, { message: 'Error', onClose });
    
    const closeButton = screen.getByText('閉じる (Close)');
    await fireEvent.click(closeButton);
    
    expect(onClose).toHaveBeenCalled();
  });

  it('should show retry button and call onRetry when clicked', async () => {
    const onRetry = vi.fn();
    render(ErrorDialog, { message: 'Error', onRetry, onClose: vi.fn() });
    
    const retryButton = screen.getByText('再試行 (Retry)');
    expect(retryButton).toBeInTheDocument();
    
    await fireEvent.click(retryButton);
    expect(onRetry).toHaveBeenCalled();
  });
});
