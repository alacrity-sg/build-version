package lib

import (
	"errors"
	"regexp"

	"github.com/go-git/go-git/v5"
	"github.com/go-git/go-git/v5/plumbing"
)

func GetLastCommit(repoPath string) (*string, error) {
	r, err := git.PlainOpen(repoPath)
	if err != nil {
		return nil, err
	}
	ref, err := r.Head()

	if err != nil {
		return nil, err
	}

	cIter, err := r.Log(&git.LogOptions{From: ref.Hash()})

	if err != nil {
		return nil, err
	}
	commit, err := cIter.Next()
	hashString := commit.Hash.String()
	return &hashString, nil
}

func GetLatestReleaseTag(repoPath string) (*string, error) {
	r, err := git.PlainOpen(repoPath)
	tags, err := r.Tags()
	if err != nil {
		return nil, err
	}
	qualifiedTag := ""
	tags.ForEach(func(t *plumbing.Reference) error {
		tagName := t.Name().Short()
		match, _ := regexp.MatchString("^v[0-9]+\\.[0-9]+\\.[0-9]+$", tagName)
		if match == true {
			qualifiedTag = tagName
		}
		return nil
	})
	if qualifiedTag == "" {
		return nil, errors.New("No qualified tag matching release regex found.")
	}
	return &qualifiedTag, nil
}

func GetLatestRCTag(repoPath string) (*string, error) {
	r, err := git.PlainOpen(repoPath)
	tags, err := r.Tags()
	if err != nil {
		return nil, err
	}
	qualifiedTag := ""
	tags.ForEach(func(t *plumbing.Reference) error {
		tagName := t.Name().Short()
		match, _ := regexp.MatchString("^v[0-9]+\\.[0-9]+\\.[0-9]+-rc\\.\\S+$", tagName)
		if match == true {
			qualifiedTag = tagName
		}
		return nil
	})
	if qualifiedTag == "" {
		return nil, errors.New("No qualified tag matching release candidate regex found.")
	}
	return &qualifiedTag, nil
}
