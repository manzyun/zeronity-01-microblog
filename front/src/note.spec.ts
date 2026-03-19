import { describe, it, expect, vi, beforeEach } from 'vitest';
import { noteApi } from './lib/api';

describe('Note Flow API', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn());
  });

  it('should call create note API and return response on success', async () => {
    const mockResponse = { id: 'note-id', content: 'test content' };
    (fetch as any).mockResolvedValue({
      status: 201,
      ok: true,
      json: async () => mockResponse
    });

    const result = await noteApi.create('test content');

    expect(fetch).toHaveBeenCalledWith('/api/notes', expect.objectContaining({
      method: 'POST',
      body: JSON.stringify({ content: 'test content' })
    }));
    expect(result).toEqual(mockResponse);
  });

  it('should call create note API with attachments', async () => {
    const attachments = [{ type: 'Image', url: 'http://example.com/image.jpg', mime_type: 'image/jpeg' }];
    const mockResponse = { id: 'note-id', content: 'test content', attachments };
    (fetch as any).mockResolvedValue({
      status: 201,
      ok: true,
      json: async () => mockResponse
    });

    const result = await noteApi.create('test content', attachments);

    expect(fetch).toHaveBeenCalledWith('/api/notes', expect.objectContaining({
      method: 'POST',
      body: JSON.stringify({ content: 'test content', attachments })
    }));
    expect(result).toEqual(mockResponse);
  });

  it('should call delete note API', async () => {
    (fetch as any).mockResolvedValue({
      status: 204,
      ok: true,
      json: async () => ({})
    });

    await noteApi.delete('note-id');

    expect(fetch).toHaveBeenCalledWith('/api/notes/note-id', expect.objectContaining({
      method: 'DELETE'
    }));
  });
});
