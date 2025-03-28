"use client";

import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  Grid,
  Tag,
  HomeIcon,
  User,
  Bell,
  PlusSquare,
  LogOut,
  Settings,
  MoreHorizontal,
  Flag,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

// Sample user data (in a real app, this would come from an API)
const userProfiles = {
  johndoe: {
    username: "johndoe",
    name: "John Doe",
    bio: "Photographer | Traveler | Coffee enthusiast\nCapturing moments and sharing stories.",
    website: "https://johndoe-portfolio.com",
    postsCount: 87,
    followersCount: 2453,
    followingCount: 735,
    avatar:
      "https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?w=150&h=150&fit=crop&crop=faces&q=80",
    isVerified: true,
    isFollowing: false,
  },
  janesmith: {
    username: "janesmith",
    name: "Jane Smith",
    bio: "Digital artist & UI designer\nCreating beautiful interfaces and illustrations.",
    website: "https://janesmith.design",
    postsCount: 124,
    followersCount: 5678,
    followingCount: 412,
    avatar:
      "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&h=150&fit=crop&crop=faces&q=80",
    isVerified: true,
    isFollowing: true,
  },
  alexj: {
    username: "alexj",
    name: "Alex Johnson",
    bio: "Software developer | Gamer | Tech enthusiast",
    website: "https://alexj.dev",
    postsCount: 56,
    followersCount: 1024,
    followingCount: 512,
    avatar:
      "https://images.unsplash.com/photo-1568602471122-7832951cc4c5?w=150&h=150&fit=crop&crop=faces&q=80",
    isVerified: false,
    isFollowing: false,
  },
};

// Generate sample posts for each user
const generatePosts = (username, count = 9) => {
  return Array.from({ length: count }, (_, i) => ({
    id: `${username}-${i + 1}`,
    image: `https://source.unsplash.com/random/600x600?sig=${username}${i}`,
    likes: Math.floor(Math.random() * 100) + 10,
    comments: Math.floor(Math.random() * 20) + 1,
  }));
};

export default function Profile() {
  const { username } = useParams();
  const [isFollowing, setIsFollowing] = useState(
    userProfiles[username]?.isFollowing || false
  );

  // If username doesn't exist in our sample data, use johndoe as default
  const profileData = userProfiles[username] || userProfiles.johndoe;
  const posts = generatePosts(profileData.username);

  const handleFollowToggle = () => {
    setIsFollowing(!isFollowing);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header/Navigation */}
      <header className="sticky top-0 z-10 bg-white border-b border-gray-200">
        <div className="container mx-auto px-4 py-2 flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold text-emerald-600">
            SocialApp
          </Link>

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
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Avatar className="h-8 w-8 cursor-pointer">
                  <AvatarImage
                    src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=32&h=32&fit=crop&crop=faces&q=80"
                    alt="Your profile"
                  />
                  <AvatarFallback>YP</AvatarFallback>
                </Avatar>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem asChild>
                  <Link to="/my-profile" className="flex items-center">
                    <User className="mr-2 h-4 w-4" />
                    Profile
                  </Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link to="/settings" className="flex items-center">
                    <Settings className="mr-2 h-4 w-4" />
                    Settings
                  </Link>
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem className="flex items-center">
                  <LogOut className="mr-2 h-4 w-4" />
                  Logout
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6">
        {/* Profile Header */}
        <div className="bg-white rounded-lg p-6 shadow-sm mb-6">
          <div className="flex flex-col md:flex-row items-center md:items-start gap-6">
            <Avatar className="h-24 w-24 md:h-36 md:w-36">
              <AvatarImage
                src={profileData.avatar}
                alt={profileData.username}
              />
              <AvatarFallback className="text-2xl">
                {profileData.name[0]}
              </AvatarFallback>
            </Avatar>

            <div className="flex-1 text-center md:text-left">
              <div className="flex flex-col md:flex-row md:items-center gap-4 mb-4">
                <div className="flex items-center justify-center md:justify-start gap-2">
                  <h1 className="text-2xl font-semibold">
                    {profileData.username}
                  </h1>
                  {profileData.isVerified && (
                    <span className="bg-blue-500 text-white rounded-full p-1 flex items-center justify-center h-5 w-5">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="3"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        className="h-3 w-3"
                      >
                        <polyline points="20 6 9 17 4 12"></polyline>
                      </svg>
                    </span>
                  )}
                </div>
                <div className="flex gap-2 justify-center md:justify-start">
                  <Button
                    className={
                      isFollowing
                        ? "bg-gray-200 text-gray-800 hover:bg-gray-300"
                        : "bg-emerald-600 hover:bg-emerald-700"
                    }
                    onClick={handleFollowToggle}
                  >
                    {isFollowing ? "Following" : "Follow"}
                  </Button>
                  <Button variant="outline">Message</Button>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="outline" size="icon">
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem>Share profile</DropdownMenuItem>
                      <DropdownMenuItem>Block user</DropdownMenuItem>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem className="text-red-600">
                        <Flag className="mr-2 h-4 w-4" />
                        Report
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              </div>

              <div className="flex justify-center md:justify-start space-x-8 mb-4">
                <div className="text-center">
                  <span className="font-semibold">
                    {profileData.postsCount}
                  </span>
                  <p className="text-gray-500">posts</p>
                </div>
                <button className="text-center">
                  <span className="font-semibold">
                    {profileData.followersCount}
                  </span>
                  <p className="text-gray-500">followers</p>
                </button>
                <button className="text-center">
                  <span className="font-semibold">
                    {profileData.followingCount}
                  </span>
                  <p className="text-gray-500">following</p>
                </button>
              </div>

              <div className="space-y-2">
                <h2 className="font-semibold">{profileData.name}</h2>
                <p className="whitespace-pre-wrap">{profileData.bio}</p>
                {profileData.website && (
                  <a
                    href={profileData.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-emerald-600 font-medium"
                  >
                    {profileData.website.replace(/^https?:\/\//, "")}
                  </a>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Profile Content Tabs */}
        <Tabs defaultValue="posts" className="w-full">
          <TabsList className="w-full grid grid-cols-2 mb-6">
            <TabsTrigger value="posts" className="flex items-center gap-2">
              <Grid className="h-4 w-4" />
              <span className="hidden sm:inline">Posts</span>
            </TabsTrigger>
            <TabsTrigger value="tagged" className="flex items-center gap-2">
              <Tag className="h-4 w-4" />
              <span className="hidden sm:inline">Tagged</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="posts" className="mt-0">
            <div className="grid grid-cols-3 gap-1 md:gap-4">
              {posts.map((post) => (
                <Link
                  key={post.id}
                  to={`/posts/${post.id}`}
                  className="relative aspect-square group overflow-hidden"
                >
                  <img
                    src={post.image || "/placeholder.svg"}
                    alt={`Post by ${profileData.username}`}
                    className="object-cover w-full h-full"
                  />
                  <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-50 transition-all flex items-center justify-center opacity-0 group-hover:opacity-100">
                    <div className="flex items-center space-x-4 text-white">
                      <div className="flex items-center">
                        <span className="font-bold mr-1">{post.likes}</span>
                        <span>❤️</span>
                      </div>
                      <div className="flex items-center">
                        <span className="font-bold mr-1">{post.comments}</span>
                        <span>💬</span>
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="tagged" className="mt-0">
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <Tag className="h-16 w-16 text-gray-300 mb-4" />
              <h3 className="text-xl font-semibold mb-2">No Photos</h3>
              <p className="text-gray-500 max-w-md">
                When {profileData.username} is tagged in photos, they'll appear
                here.
              </p>
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
