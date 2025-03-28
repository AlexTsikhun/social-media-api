"use client";

import { useState, useRef, useEffect } from "react";
import { Link, useParams } from "react-router-dom";
import {
  Heart,
  MessageCircle,
  Bookmark,
  Share2,
  MoreHorizontal,
  HomeIcon,
  User,
  Bell,
  PlusSquare,
  Smile,
  ArrowLeft,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Textarea } from "@/components/ui/textarea";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Separator } from "@/components/ui/separator";

// Sample post data with numeric IDs
const posts = {
  1: {
    id: "1",
    user: {
      username: "johndoe",
      name: "John Doe",
      avatar:
        "https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?w=150&h=150&fit=crop&crop=faces&q=80",
      isVerified: true,
    },
    image:
      "https://images.unsplash.com/photo-1501854140801-50d01698950b?w=1200&h=1200&fit=crop&q=80",
    caption:
      "Beautiful sunset over the mountains. Nature at its finest. #sunset #mountains #nature #photography",
    location: "Rocky Mountains, Colorado",
    likes: 1243,
    isLiked: false,
    isSaved: false,
    createdAt: "2023-06-15T18:30:00Z",
    comments: [
      {
        id: "c1",
        user: {
          username: "janesmith",
          avatar:
            "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&h=150&fit=crop&crop=faces&q=80",
        },
        text: "This is absolutely stunning! 😍 Where exactly in the Rockies was this taken?",
        likes: 24,
        createdAt: "2023-06-15T19:15:00Z",
        replies: [],
      },
      {
        id: "c2",
        user: {
          username: "alexj",
          avatar:
            "https://images.unsplash.com/photo-1568602471122-7832951cc4c5?w=150&h=150&fit=crop&crop=faces&q=80",
        },
        text: "The colors in this photo are incredible. What camera did you use?",
        likes: 8,
        createdAt: "2023-06-15T20:45:00Z",
        replies: [],
      },
    ],
  },
  2: {
    id: "2",
    user: {
      username: "janesmith",
      name: "Jane Smith",
      avatar:
        "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&h=150&fit=crop&crop=faces&q=80",
      isVerified: true,
    },
    image:
      "https://images.unsplash.com/photo-1484723091739-30a097e8f929?w=1200&h=1200&fit=crop&q=80",
    caption:
      "Homemade avocado toast with poached eggs and microgreens. The perfect start to any day! #foodie #breakfast #avocadotoast #healthyeating",
    location: "Home Kitchen",
    likes: 876,
    isLiked: true,
    isSaved: true,
    createdAt: "2023-06-17T09:15:00Z",
    comments: [
      {
        id: "c4",
        user: {
          username: "mikebrown",
          avatar:
            "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=faces&q=80",
        },
        text: "This looks delicious! I need to try making this tomorrow.",
        likes: 15,
        createdAt: "2023-06-17T09:45:00Z",
        replies: [],
      },
      {
        id: "c5",
        user: {
          username: "emmawatson",
          avatar:
            "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&h=150&fit=crop&crop=faces&q=80",
        },
        text: "Your food photography skills are amazing! Any tips?",
        likes: 32,
        createdAt: "2023-06-17T11:30:00Z",
        replies: [],
      },
    ],
  },
  3: {
    id: "3",
    user: {
      username: "alexj",
      name: "Alex Johnson",
      avatar:
        "https://images.unsplash.com/photo-1568602471122-7832951cc4c5?w=150&h=150&fit=crop&crop=faces&q=80",
      isVerified: false,
    },
    image:
      "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=1200&h=1200&fit=crop&q=80",
    caption:
      "Late night coding session. Building something exciting! #coding #developer #javascript #webdev",
    location: "Tech Hub Coworking",
    likes: 543,
    isLiked: false,
    isSaved: false,
    createdAt: "2023-06-18T23:45:00Z",
    comments: [
      {
        id: "c6",
        user: {
          username: "johndoe",
          avatar:
            "https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?w=150&h=150&fit=crop&crop=faces&q=80",
        },
        text: "What are you working on? Looks interesting!",
        likes: 7,
        createdAt: "2023-06-19T00:15:00Z",
        replies: [],
      },
    ],
  },
};

// Function to format date
const formatDate = (dateString) => {
  const options = { year: "numeric", month: "long", day: "numeric" };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

// Function to get related posts
const getRelatedPosts = (currentPostId) => {
  return Object.values(posts)
    .filter((post) => post.id !== currentPostId)
    .slice(0, 3);
};

export default function PostDetail() {
  // Changed from postId to id to match your route parameter
  const { id } = useParams();

  // Default to first post if ID not found
  const defaultPost = posts[id] || Object.values(posts)[0];

  const [post, setPost] = useState(defaultPost);
  const [comment, setComment] = useState("");
  const [isLiked, setIsLiked] = useState(defaultPost.isLiked);
  const [isSaved, setIsSaved] = useState(defaultPost.isSaved);
  const [likesCount, setLikesCount] = useState(defaultPost.likes);
  const commentInputRef = useRef(null);
  const relatedPosts = getRelatedPosts(post.id);

  useEffect(() => {
    // Update post data if id changes and exists in our data
    if (posts[id]) {
      setPost(posts[id]);
      setIsLiked(posts[id].isLiked);
      setIsSaved(posts[id].isSaved);
      setLikesCount(posts[id].likes);
    }
  }, [id]);

  const handleLike = () => {
    setIsLiked(!isLiked);
    setLikesCount((prev) => (isLiked ? prev - 1 : prev + 1));
  };

  const handleSave = () => {
    setIsSaved(!isSaved);
  };

  const handleCommentSubmit = (e) => {
    e.preventDefault();
    if (!comment.trim()) return;

    // In a real app, you would send this to an API
    const newComment = {
      id: `c${Date.now()}`,
      user: {
        username: "yourusername",
        avatar:
          "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&h=150&fit=crop&crop=faces&q=80",
      },
      text: comment,
      likes: 0,
      createdAt: new Date().toISOString(),
      replies: [],
    };

    setPost((prev) => ({
      ...prev,
      comments: [newComment, ...prev.comments],
    }));
    setComment("");
  };

  const focusCommentInput = () => {
    if (commentInputRef.current) {
      commentInputRef.current.focus();
    }
  };

  // If no post is found, show a message
  if (!post) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center p-8">
          <h1 className="text-2xl font-bold mb-4">Post Not Found</h1>
          <p className="mb-6">
            The post you're looking for doesn't exist or has been removed.
          </p>
          <Button asChild>
            <Link to="/">Go Back Home</Link>
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header/Navigation */}
      <header className="sticky top-0 z-10 bg-white border-b border-gray-200">
        <div className="container mx-auto px-4 py-2 flex items-center justify-between">
          <div className="flex items-center">
            <Button
              variant="ghost"
              size="icon"
              asChild
              className="md:hidden mr-2"
            >
              <Link to="/">
                <ArrowLeft className="h-5 w-5" />
              </Link>
            </Button>
            <Link to="/" className="text-2xl font-bold text-emerald-600">
              SocialApp
            </Link>
          </div>

          <div className="flex items-center space-x-4">
            <Button variant="ghost" size="icon" asChild>
              <Link to="/">
                <HomeIcon className="h-5 w-5" />
              </Link>
            </Button>
            <Button variant="ghost" size="icon">
              <Bell className="h-5 w-5" />
            </Button>
            <Button variant="ghost" size="icon">
              <PlusSquare className="h-5 w-5" />
            </Button>
            <Button variant="ghost" size="icon" asChild>
              <Link to="/my-profile">
                <User className="h-5 w-5" />
              </Link>
            </Button>
            <Avatar className="h-8 w-8">
              <AvatarImage
                src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=32&h=32&fit=crop&crop=faces&q=80"
                alt="Your profile"
              />
              <AvatarFallback>YP</AvatarFallback>
            </Avatar>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6">
        <div className="max-w-4xl mx-auto">
          {/* Post Detail Card */}
          <div className="bg-white rounded-lg shadow-sm overflow-hidden mb-8">
            <div className="md:flex">
              {/* Post Image - Takes full width on mobile, half on desktop */}
              <div className="md:w-1/2">
                <img
                  src={post.image || "/placeholder.svg"}
                  alt={post.caption}
                  className="w-full h-auto md:h-full object-cover"
                />
              </div>

              {/* Post Details - Takes full width on mobile, half on desktop */}
              <div className="md:w-1/2 flex flex-col">
                {/* Post Header */}
                <div className="p-4 border-b flex items-center justify-between">
                  <div className="flex items-center">
                    <Link to={`/profile/${post.user.username}`}>
                      <Avatar className="h-8 w-8 mr-3">
                        <AvatarImage
                          src={post.user.avatar}
                          alt={post.user.username}
                        />
                        <AvatarFallback>
                          {post.user.username[0].toUpperCase()}
                        </AvatarFallback>
                      </Avatar>
                    </Link>
                    <div>
                      <Link
                        to={`/profile/${post.user.username}`}
                        className="font-semibold hover:underline flex items-center"
                      >
                        {post.user.username}
                        {post.user.isVerified && (
                          <span className="ml-1 bg-blue-500 text-white rounded-full p-0.5 flex items-center justify-center h-4 w-4">
                            <svg
                              xmlns="http://www.w3.org/2000/svg"
                              viewBox="0 0 24 24"
                              fill="none"
                              stroke="currentColor"
                              strokeWidth="3"
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              className="h-2.5 w-2.5"
                            >
                              <polyline points="20 6 9 17 4 12"></polyline>
                            </svg>
                          </span>
                        )}
                      </Link>
                      {post.location && (
                        <p className="text-xs text-gray-500">{post.location}</p>
                      )}
                    </div>
                  </div>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="icon">
                        <MoreHorizontal className="h-5 w-5" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem>Copy link</DropdownMenuItem>
                      <DropdownMenuItem>Share to...</DropdownMenuItem>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem className="text-red-600">
                        Report
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>

                {/* Comments Section */}
                <div className="flex-1 overflow-y-auto p-4 space-y-4 max-h-96">
                  {/* Caption */}
                  <div className="flex space-x-3">
                    <Avatar className="h-8 w-8 flex-shrink-0">
                      <AvatarImage
                        src={post.user.avatar}
                        alt={post.user.username}
                      />
                      <AvatarFallback>
                        {post.user.username[0].toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                    <div>
                      <p>
                        <Link
                          to={`/profile/${post.user.username}`}
                          className="font-semibold hover:underline mr-2"
                        >
                          {post.user.username}
                        </Link>
                        {post.caption}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        {formatDate(post.createdAt)}
                      </p>
                    </div>
                  </div>

                  <Separator />

                  {/* Comments */}
                  {post.comments.map((comment) => (
                    <div key={comment.id} className="flex space-x-3">
                      <Avatar className="h-8 w-8 flex-shrink-0">
                        <AvatarImage
                          src={comment.user.avatar}
                          alt={comment.user.username}
                        />
                        <AvatarFallback>
                          {comment.user.username[0].toUpperCase()}
                        </AvatarFallback>
                      </Avatar>
                      <div className="flex-1">
                        <p>
                          <Link
                            to={`/profile/${comment.user.username}`}
                            className="font-semibold hover:underline mr-2"
                          >
                            {comment.user.username}
                          </Link>
                          {comment.text}
                        </p>
                        <div className="flex items-center space-x-4 mt-1 text-xs text-gray-500">
                          <span>{formatDate(comment.createdAt)}</span>
                          <button>{comment.likes} likes</button>
                          <button>Reply</button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Post Actions */}
                <div className="p-4 border-t">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-4">
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={handleLike}
                        className={isLiked ? "text-red-500" : ""}
                      >
                        <Heart
                          className={`h-6 w-6 ${isLiked ? "fill-current" : ""}`}
                        />
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={focusCommentInput}
                      >
                        <MessageCircle className="h-6 w-6" />
                      </Button>
                      <Button variant="ghost" size="icon">
                        <Share2 className="h-6 w-6" />
                      </Button>
                    </div>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={handleSave}
                      className={isSaved ? "text-yellow-500" : ""}
                    >
                      <Bookmark
                        className={`h-6 w-6 ${isSaved ? "fill-current" : ""}`}
                      />
                    </Button>
                  </div>

                  <p className="font-semibold mb-1">{likesCount} likes</p>
                  <p className="text-xs text-gray-500 mb-4">
                    {formatDate(post.createdAt)}
                  </p>

                  {/* Add Comment Form */}
                  <form
                    onSubmit={handleCommentSubmit}
                    className="flex items-center space-x-2"
                  >
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      className="flex-shrink-0"
                    >
                      <Smile className="h-5 w-5" />
                    </Button>
                    <Textarea
                      ref={commentInputRef}
                      placeholder="Add a comment..."
                      value={comment}
                      onChange={(e) => setComment(e.target.value)}
                      className="min-h-0 h-10 py-2 resize-none"
                    />
                    <Button
                      type="submit"
                      variant="ghost"
                      size="sm"
                      className="text-emerald-600 font-semibold"
                      disabled={!comment.trim()}
                    >
                      Post
                    </Button>
                  </form>
                </div>
              </div>
            </div>
          </div>

          {/* Related Posts */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold mb-4">
              More posts you might like
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
              {relatedPosts.map((post) => (
                <Link
                  key={post.id}
                  to={`/posts/${post.id}`}
                  className="relative aspect-square group overflow-hidden rounded-lg"
                >
                  <img
                    src={post.image || "/placeholder.svg"}
                    alt={post.caption}
                    className="object-cover w-full h-full"
                  />
                  <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-50 transition-all flex items-center justify-center opacity-0 group-hover:opacity-100">
                    <div className="flex items-center space-x-4 text-white">
                      <div className="flex items-center">
                        <span className="font-bold mr-1">{post.likes}</span>
                        <Heart className="h-4 w-4 fill-current" />
                      </div>
                      <div className="flex items-center">
                        <span className="font-bold mr-1">
                          {post.comments.length}
                        </span>
                        <MessageCircle className="h-4 w-4" />
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
