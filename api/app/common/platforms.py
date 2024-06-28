from dataclasses import dataclass


@dataclass
class InbangPlatforms:
    platform_choices = [
        ("youtube", "YouTube"),
        ("chzzk", "Chzzk"),
        ("afreecatv", "AfreecaTV"),
        ("twitch", "Twitch"),
    ]


@dataclass
class OAuthPlatforms:
    platform_choices = [
        ("none", "None"),  # None ( default, A user directly signed in with our site )
        ("google", "Google"),  # Google
        ("naver", "Naver"),  # Naver
    ]
