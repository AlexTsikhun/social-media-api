"use client";

import { useState } from "react";
import { Link } from "react-router-dom";
import {
  Settings,
  Grid,
  Bookmark,
  Tag,
  Edit,
  HomeIcon,
  User,
  Bell,
  PlusSquare,
  LogOut,
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
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

// Sample user data
const userData = {
  username: "yourusername",
  name: "Your Full Name",
  bio: "Photography enthusiast | Travel lover | Software developer",
  website: "https://yourwebsite.com",
  postsCount: 42,
  followersCount: 1024,
  followingCount: 512,
  avatar: "/placeholder.svg?height=150&width=150",
};

// Sample posts data
const posts = Array.from({ length: 9 }, (_, i) => ({
  id: i + 1,
  image: `/placeholder.svg?height=300&width=300&text=Post ${i + 1}`,
  likes: Math.floor(Math.random() * 100) + 10,
  comments: Math.floor(Math.random() * 20) + 1,
}));

// Sample saved posts
const savedPosts = Array.from({ length: 6 }, (_, i) => ({
  id: i + 100,
  image: `/placeholder.svg?height=300&width=300&text=Saved ${i + 1}`,
  likes: Math.floor(Math.random() * 100) + 10,
  comments: Math.floor(Math.random() * 20) + 1,
}));

export default function MyProfile() {
  const [activeTab, setActiveTab] = useState("posts");
  const [profileData, setProfileData] = useState(userData);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [editForm, setEditForm] = useState({
    name: userData.name,
    username: userData.username,
    website: userData.website,
    bio: userData.bio,
  });

  const handleEditSubmit = (e) => {
    e.preventDefault();
    setProfileData({
      ...profileData,
      name: editForm.name,
      username: editForm.username,
      website: editForm.website,
      bio: editForm.bio,
    });
    setIsEditDialogOpen(false);
  };

  const handleEditChange = (e) => {
    const { name, value } = e.target;
    setEditForm((prev) => ({
      ...prev,
      [name]: value,
    }));
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
                <User className="h-5 w-5 text-emerald-600" />
              </Link>
            </Button>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Avatar className="h-8 w-8 cursor-pointer">
                  <AvatarImage
                    src={profileData.avatar}
                    alt={profileData.username}
                  />
                  <AvatarFallback>{profileData.name[0]}</AvatarFallback>
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
                <h1 className="text-2xl font-semibold">
                  {profileData.username}
                </h1>
                <div className="flex gap-2 justify-center md:justify-start">
                  <Dialog
                    open={isEditDialogOpen}
                    onOpenChange={setIsEditDialogOpen}
                  >
                    <DialogTrigger asChild>
                      <Button className="bg-emerald-600 hover:bg-emerald-700">
                        <Edit className="h-4 w-4 mr-2" />
                        Edit Profile
                      </Button>
                    </DialogTrigger>
                    <DialogContent>
                      <DialogHeader>
                        <DialogTitle>Edit Profile</DialogTitle>
                      </DialogHeader>
                      <form
                        onSubmit={handleEditSubmit}
                        className="space-y-4 mt-4"
                      >
                        <div className="space-y-2">
                          <Label htmlFor="name">Name</Label>
                          <Input
                            id="name"
                            name="name"
                            value={editForm.name}
                            onChange={handleEditChange}
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="username">Username</Label>
                          <Input
                            id="username"
                            name="username"
                            value={editForm.username}
                            onChange={handleEditChange}
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="website">Website</Label>
                          <Input
                            id="website"
                            name="website"
                            value={editForm.website}
                            onChange={handleEditChange}
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="bio">Bio</Label>
                          <Textarea
                            id="bio"
                            name="bio"
                            value={editForm.bio}
                            onChange={handleEditChange}
                            rows={3}
                          />
                        </div>
                        <div className="flex justify-end gap-2">
                          <Button
                            type="button"
                            variant="outline"
                            onClick={() => setIsEditDialogOpen(false)}
                          >
                            Cancel
                          </Button>
                          <Button
                            type="submit"
                            className="bg-emerald-600 hover:bg-emerald-700"
                          >
                            Save Changes
                          </Button>
                        </div>
                      </form>
                    </DialogContent>
                  </Dialog>

                  <Button variant="outline" asChild>
                    <Link to="/settings">
                      <Settings className="h-4 w-4" />
                    </Link>
                  </Button>
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
        <Tabs
          defaultValue="posts"
          className="w-full"
          onValueChange={setActiveTab}
        >
          <TabsList className="w-full grid grid-cols-3 mb-6">
            <TabsTrigger value="posts" className="flex items-center gap-2">
              <Grid className="h-4 w-4" />
              <span className="hidden sm:inline">Posts</span>
            </TabsTrigger>
            <TabsTrigger value="saved" className="flex items-center gap-2">
              <Bookmark className="h-4 w-4" />
              <span className="hidden sm:inline">Saved</span>
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
                  to={`/post/${post.id}`}
                  className="relative aspect-square group overflow-hidden"
                >
                  <img
                    src={post.image || "/placeholder.svg"}
                    alt={`Post ${post.id}`}
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

          <TabsContent value="saved" className="mt-0">
            <div className="grid grid-cols-3 gap-1 md:gap-4">
              {savedPosts.map((post) => (
                <Link
                  key={post.id}
                  to={`/post/${post.id}`}
                  className="relative aspect-square group overflow-hidden"
                >
                  <img
                    src={post.image || "/placeholder.svg"}
                    alt={`Saved post ${post.id}`}
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
                When people tag you in photos, they'll appear here.
              </p>
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
