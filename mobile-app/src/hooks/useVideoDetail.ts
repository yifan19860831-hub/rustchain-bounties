/**
 * Video Detail Hook
 * Fetches and manages single video data
 */

import { useState, useEffect, useCallback } from 'react';
import { api } from '../api/client';
import { Video, Comment } from '../types/api';

interface UseVideoDetailResult {
  video: Video | null;
  comments: Comment[];
  isLoading: boolean;
  error: string | null;
  refresh: () => Promise<void>;
  vote: (value: 1 | -1) => Promise<void>;
  addComment: (content: string) => Promise<void>;
  streamUrl: string | null;
  thumbnailUrl: string | null;
}

export function useVideoDetail(videoId: string | null): UseVideoDetailResult {
  const [video, setVideo] = useState<Video | null>(null);
  const [comments, setComments] = useState<Comment[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchVideo = useCallback(async () => {
    if (!videoId) return;
    
    try {
      setIsLoading(true);
      setError(null);
      
      const [videoData, commentsData] = await Promise.all([
        api.getVideo(videoId),
        api.getComments(videoId),
      ]);
      
      setVideo(videoData);
      setComments(commentsData);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load video';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }, [videoId]);

  const refresh = useCallback(async () => {
    await fetchVideo();
  }, [fetchVideo]);

  const vote = useCallback(async (value: 1 | -1) => {
    if (!videoId) return;
    
    try {
      await api.vote(videoId, { vote: value });
      // Optimistically update local state
      setVideo(prev => prev ? {
        ...prev,
        likes: value === 1 ? prev.likes + 1 : prev.likes,
        dislikes: value === -1 ? prev.dislikes + 1 : prev.dislikes,
      } : null);
    } catch (err) {
      console.error('Vote failed:', err);
    }
  }, [videoId]);

  const addComment = useCallback(async (content: string) => {
    if (!videoId) return;
    
    try {
      const newComment = await api.addComment(videoId, { content });
      setComments(prev => [newComment, ...prev]);
    } catch (err) {
      console.error('Comment failed:', err);
      throw err;
    }
  }, [videoId]);

  useEffect(() => {
    fetchVideo();
  }, [videoId]); // eslint-disable-line react-hooks/exhaustive-deps

  const streamUrl = videoId ? api.getVideoStreamUrl(videoId) : null;
  const thumbnailUrl = videoId ? api.getThumbnailUrl(videoId) : null;

  return {
    video,
    comments,
    isLoading,
    error,
    refresh,
    vote,
    addComment,
    streamUrl,
    thumbnailUrl,
  };
}
