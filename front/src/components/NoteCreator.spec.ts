import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/svelte';
import NoteCreator from './NoteCreator.svelte';
import { noteApi } from '../lib/api';

vi.mock('../lib/api', () => ({
  noteApi: {
    create: vi.fn()
  }
}));

describe('NoteCreator Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should call noteApi.create when submit button is clicked', async () => {
    (noteApi.create as any).mockResolvedValue({ id: 'new-note' });
    
    render(NoteCreator);
    
    const textarea = screen.getByPlaceholderText("What's on your mind?");
    await fireEvent.input(textarea, { target: { value: 'Hello world' } });
    
    const submitButton = screen.getByText('Post Note');
    await fireEvent.click(submitButton);
    
    expect(noteApi.create).toHaveBeenCalledWith('Hello world', undefined);
    
    await waitFor(() => {
      expect(textarea).toHaveValue('');
    });
  });

  it('should show ErrorDialog when API fails', async () => {
    (noteApi.create as any).mockRejectedValue(new Error('API Failure'));
    
    render(NoteCreator);
    
    const textarea = screen.getByPlaceholderText("What's on your mind?");
    await fireEvent.input(textarea, { target: { value: 'Error trigger' } });
    
    const submitButton = screen.getByText('Post Note');
    await fireEvent.click(submitButton);
    
    expect(noteApi.create).toHaveBeenCalled();
    
    const errorDialog = await screen.findByText('API Failure');
    expect(errorDialog).toBeInTheDocument();
    
    const retryButton = screen.getByText('再試行 (Retry)');
    expect(retryButton).toBeInTheDocument();
  });

  it('should call noteApi.create again when retry is clicked', async () => {
    (noteApi.create as any)
      .mockRejectedValueOnce(new Error('First failure'))
      .mockResolvedValueOnce({ id: 'success' });
    
    render(NoteCreator);
    
    const textarea = screen.getByPlaceholderText("What's on your mind?");
    await fireEvent.input(textarea, { target: { value: 'Retry test' } });
    
    await fireEvent.click(screen.getByText('Post Note'));
    
    await screen.findByText('First failure');
    const retryButton = screen.getByText('再試行 (Retry)');
    
    await fireEvent.click(retryButton);
    
    expect(noteApi.create).toHaveBeenCalledTimes(2);
    expect(noteApi.create).toHaveBeenNthCalledWith(2, 'Retry test', undefined);
  });
});
