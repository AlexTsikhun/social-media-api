"use client";

import { useState } from "react";
import { Eye, EyeOff, Github, Twitter } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";

export default function RegisterPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [fullName, setFullName] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [agreeTerms, setAgreeTerms] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1500));

    console.log({ fullName, username, email, password, agreeTerms });
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen flex flex-col md:flex-row">
      {/* Left side - Visual */}
      <div className="hidden md:flex md:w-1/2 bg-[#2E7D32] p-8 items-center justify-center">
        <div className="max-w-md">
          <div className="grid grid-cols-3 gap-2">
            {Array.from({ length: 9 }).map((_, i) => (
              <div
                key={i}
                className="aspect-square rounded-2xl bg-white/10 backdrop-blur-sm"
                style={{
                  transform: `rotate(${Math.random() * 10 - 5}deg)`,
                  opacity: 0.7 + Math.random() * 0.3,
                }}
              />
            ))}
          </div>
          <h1 className="text-white text-4xl font-bold mt-8">
            Discover ideas and get inspired
          </h1>
          <p className="text-white/80 mt-4">
            Join our community and start creating your collections today.
          </p>
        </div>
      </div>

      {/* Right side - Registration form */}
      <div className="flex-1 flex items-center justify-center p-8 md:p-12 lg:p-16">
        <div className="w-full max-w-md space-y-8 mx-auto">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold">Create an account</h2>
            <p className="mt-2 text-muted-foreground">
              Fill in your details below
            </p>
          </div>

          <form onSubmit={handleSubmit} className="mt-8 space-y-6">
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="fullName">Full Name</Label>
                <Input
                  id="fullName"
                  type="text"
                  placeholder="John Doe"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  required
                  className="h-12 rounded-xl"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="username">Username</Label>
                <Input
                  id="username"
                  type="text"
                  placeholder="johndoe"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                  className="h-12 rounded-xl"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="h-12 rounded-xl"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <div className="relative">
                  <Input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    className="h-12 rounded-xl pr-10"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground"
                  >
                    {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
              </div>

              <div className="flex items-center space-x-2">
                <Checkbox
                  id="agreeTerms"
                  checked={agreeTerms}
                  onCheckedChange={setAgreeTerms}
                />
                <Label
                  htmlFor="agreeTerms"
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                  I agree to the Terms of Service and Privacy Policy
                </Label>
              </div>
            </div>

            <Button
              type="submit"
              className="w-full h-12 rounded-xl bg-[#2E7D32] hover:bg-[#225A25] text-white"
              disabled={isLoading || !agreeTerms}
            >
              {isLoading ? "Signing up..." : "Sign up"}
            </Button>

            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-muted"></div>
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-background px-2 text-muted-foreground">
                  Or continue with
                </span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <Button variant="outline" className="h-12 rounded-xl">
                <Github className="mr-2 h-4 w-4" />
                Github
              </Button>
              <Button variant="outline" className="h-12 rounded-xl">
                <Twitter className="mr-2 h-4 w-4" />
                Twitter
              </Button>
            </div>
          </form>

          <p className="text-center text-sm text-muted-foreground mt-6">
            Already have an account?{" "}
            <a
              href="/login"
              className="font-medium text-[#2E7D32] hover:text-[#225A25]"
            >
              Sign in
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
