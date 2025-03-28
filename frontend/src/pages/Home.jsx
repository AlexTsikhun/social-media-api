"use client";

import { useState } from "react";
import { Link } from "react-router-dom";
import {
  Heart,
  MessageCircle,
  Bookmark,
  MoreHorizontal,
  Search,
  HomeIcon,
  User,
  Bell,
  PlusSquare,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
} from "@/components/ui/card";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

// Sample data for posts
const posts = [
  {
    id: 1,
    user: {
      name: "John Doe",
      username: "johndoe",
      avatar: "https://randomuser.me/api/portraits/men/1.jpg",
    },
    image: "https://picsum.photos/200/300",
    caption: "Beautiful day in the park! #nature #relax",
    likes: 124,
    comments: 23,
    timeAgo: "2h",
  },
  {
    id: 2,
    user: {
      name: "Jane Smith",
      username: "janesmith",
      avatar: "https://randomuser.me/api/portraits/women/2.jpg",
    },
    image: "https://picsum.photos/200/300",
    caption:
      "Just finished this amazing book! Highly recommend it to everyone. #reading #books",
    likes: 89,
    comments: 12,
    timeAgo: "4h",
  },
  {
    id: 3,
    user: {
      name: "Alex Johnson",
      username: "alexj",
      avatar: "https://randomuser.me/api/portraits/men/3.jpg",
    },
    image: "https://picsum.photos/200/300",
    caption: "Coding all night long! #developer #programming",
    likes: 56,
    comments: 8,
    timeAgo: "6h",
  },
];

// Sample data for stories
const stories = [
  {
    id: 1,
    username: "johndoe",
    avatar: "https://randomuser.me/api/portraits/men/4.jpg",
    hasUnseenStory: true,
  },
  {
    id: 2,
    username: "janesmith",
    avatar: "https://randomuser.me/api/portraits/women/5.jpg",
    hasUnseenStory: true,
  },
  {
    id: 3,
    username: "alexj",
    avatar: "https://randomuser.me/api/portraits/men/6.jpg",
    hasUnseenStory: false,
  },
  {
    id: 4,
    username: "sarahp",
    avatar: "https://randomuser.me/api/portraits/women/7.jpg",
    hasUnseenStory: true,
  },
  {
    id: 5,
    username: "mikebrown",
    avatar: "https://randomuser.me/api/portraits/men/8.jpg",
    hasUnseenStory: false,
  },
  {
    id: 6,
    username: "emmawatson",
    avatar: "https://randomuser.me/api/portraits/women/9.jpg",
    hasUnseenStory: true,
  },
];


export default function Home() {
  const [searchQuery, setSearchQuery] = useState("");

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header/Navigation */}
      <header className="sticky top-0 z-10 bg-white border-b border-gray-200">
        <div className="container mx-auto px-4 py-2 flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold text-emerald-600">
            SocialApp
          </Link>

          <div className="hidden md:block w-64">
            <div className="relative">
              <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <Input
                type="text"
                placeholder="Search"
                className="pl-8 h-9"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <Button variant="ghost" size="icon" asChild>
              <Link to="/">
                <HomeIcon className="h-5 w-5 text-emerald-600" />
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
                src="https://randomuser.me/api/portraits/women/9.jpg?height=32&width=32"
                alt="User"
              />
              <AvatarFallback>U</AvatarFallback>
            </Avatar>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6 grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Main content - Posts */}
        <div className="md:col-span-2 space-y-6">
          {/* Stories */}
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <h2 className="font-semibold mb-4">Stories</h2>
            <div className="flex space-x-4 overflow-x-auto pb-2">
              {stories.map((story) => (
                <div
                  key={story.id}
                  className="flex flex-col items-center space-y-1 flex-shrink-0"
                >
                  <div
                    className={`rounded-full p-[2px] ${
                      story.hasUnseenStory
                        ? "bg-gradient-to-r from-emerald-500 to-green-500"
                        : "bg-gray-200"
                    }`}
                  >
                    <Avatar className="h-14 w-14 border-2 border-white">
                      <AvatarImage src={story.avatar} alt={story.username} />
                      <AvatarFallback>
                        {story.username[0].toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                  </div>
                  <span className="text-xs">{story.username}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Posts */}
          {posts.map((post) => (
            <Card key={post.id} className="overflow-hidden">
              <CardHeader className="p-4 flex flex-row items-center space-x-4">
                <Avatar>
                  <AvatarImage src={post.user.avatar} alt={post.user.name} />
                  <AvatarFallback>{post.user.name[0]}</AvatarFallback>
                </Avatar>
                <div className="flex-1">
                  <Link
                    to={`/profile/${post.user.username}`}
                    className="font-semibold hover:underline"
                  >
                    {post.user.name}
                  </Link>
                </div>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon">
                      <MoreHorizontal className="h-5 w-5" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem>Save post</DropdownMenuItem>
                    <DropdownMenuItem>Hide post</DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem className="text-red-600">
                      Report
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </CardHeader>
              <Link to={`/post/${post.id}`}>
                <img
                  src={
                    post.image ||
                    "/https://randomuser.me/api/portraits/women/9.jpg"
                  }
                  alt="Post"
                  className="w-full object-cover aspect-square"
                />
              </Link>
              <CardFooter className="p-4 flex flex-col space-y-3">
                <div className="flex items-center justify-between w-full">
                  <div className="flex items-center space-x-2">
                    <Button variant="ghost" size="icon">
                      <Heart className="h-6 w-6" />
                    </Button>
                    <Button variant="ghost" size="icon">
                      <MessageCircle className="h-6 w-6" />
                    </Button>
                  </div>
                  <Button variant="ghost" size="icon">
                    <Bookmark className="h-6 w-6" />
                  </Button>
                </div>
                <div>
                  <p className="font-semibold">{post.likes} likes</p>
                  <div className="mt-1">
                    <span className="font-semibold">{post.user.username}</span>{" "}
                    <span>{post.caption}</span>
                  </div>
                  <Link
                    to={`/post/${post.id}`}
                    className="text-gray-500 text-sm mt-1 block"
                  >
                    View all {post.comments} comments
                  </Link>
                  <p className="text-gray-400 text-xs mt-1">{post.timeAgo}</p>
                </div>
              </CardFooter>
            </Card>
          ))}
        </div>

        {/* Sidebar */}
        <div className="hidden md:block space-y-6">
          {/* User profile summary */}
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <div className="flex items-center space-x-4">
              <Avatar className="h-12 w-12">
                <AvatarImage
                  src="https://randomuser.me/api/portraits/women/9.jpg?height=48&width=48"
                  alt="Your profile"
                />
                <AvatarFallback>YP</AvatarFallback>
              </Avatar>
              <div>
                <Link
                  to="/my-profile"
                  className="font-semibold hover:underline"
                >
                  yourusername
                </Link>
                <p className="text-gray-500 text-sm">Your Name</p>
              </div>
            </div>
          </div>

          {/* Suggestions */}
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-gray-500 font-semibold">
                Suggestions For You
              </h3>
              <Button variant="link" className="text-xs p-0 h-auto">
                See All
              </Button>
            </div>

            <div className="space-y-4">
              {[1, 2, 3, 4, 5].map((i) => (
                <div key={i} className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <Avatar className="h-8 w-8">
                      <AvatarImage
                        src={`https://randomuser.me/api/portraits/women/9.jpg?height=32&width=32&text=${i}`}
                        alt={`Suggested user ${i}`}
                      />
                      <AvatarFallback>U{i}</AvatarFallback>
                    </Avatar>
                    <div>
                      <p className="text-sm font-semibold">user{i}</p>
                      <p className="text-xs text-gray-500">Suggested for you</p>
                    </div>
                  </div>
                  <Button
                    variant="link"
                    size="sm"
                    className="text-emerald-600 p-0 h-auto"
                  >
                    Follow
                  </Button>
                </div>
              ))}
            </div>
          </div>

          {/* Footer links */}
          <div className="text-xs text-gray-400">
            <div className="flex flex-wrap gap-2 mb-4">
              <Link to="#" className="hover:underline">
                About
              </Link>
              <span>•</span>
              <Link to="#" className="hover:underline">
                Help
              </Link>
              <span>•</span>
              <Link to="#" className="hover:underline">
                Press
              </Link>
              <span>•</span>
              <Link to="#" className="hover:underline">
                API
              </Link>
              <span>•</span>
              <Link to="#" className="hover:underline">
                Jobs
              </Link>
              <span>•</span>
              <Link to="#" className="hover:underline">
                Privacy
              </Link>
              <span>•</span>
              <Link to="#" className="hover:underline">
                Terms
              </Link>
            </div>
            <p>© 2023 SOCIALAPP</p>
          </div>
        </div>
      </main>
    </div>
  );
}
